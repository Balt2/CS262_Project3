from concurrent import futures
import time

import config 
from db import DB
import grpc
import messages_pb2
import messages_pb2_grpc
import server_messages_pb2
import server_messages_pb2_grpc

import server_utils

class ServerExchange(server_messages_pb2_grpc.ServerExchange):
    def __init__(self):
        self.update_time = time.time()

    def SyncDB(self, request, context):
        response = server_messages_pb2.SyncDBResponse()
        response.update_time = self.update_time
        return response

class MessageExchange(messages_pb2_grpc.MessageExchange):
    def __init__(self, db):
        self.db = db
        self.logical_clock = 1
        self.update_time()

    def update_time(self):
        print("UPDATE TIME")
        pass
    
    def ListAccounts(self, request, context):
        response_code, accounts = self.db.listAccounts()
        response = messages_pb2.ListAccountsResponse()
        search_pattern = request.search_pattern
        for act in accounts:
            username = act[0]
            if server_utils.should_include_account(username, search_pattern):
                account_obj = messages_pb2.Account(name=username)
                response.accounts.append(account_obj)

        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time()
        print("SERVER RESPONDED: ")
        return response

    def SendMessage(self, request, context):
        response_code, delivered = self.db.insertMessage(
            request.sender_id,
            request.receiver_id,
            request.message
        )
        
        response = messages_pb2.SendMessageResponse(response_code=response_code, delivered=delivered)
        
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time()
        
        return response

    def RequestMessages(self, request, context):
        response_code, txt = self.db.getMessagesForChat(
            request.sender_id,
            request.receiver_id,
        )
        response = messages_pb2.RequestMessagesResponse(response_code=response_code)
        if response_code == 200:
            for msg in txt:

                timestamp = server_utils.timestamp_to_string(msg[5])

                message_obj = messages_pb2.Message(sender_id=msg[1], receiver_id=msg[2], message=msg[3], timestamp = timestamp)
                response.messages.append(message_obj)
        elif response_code == 404:
            response.error = txt
        
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time()
        return response

    def CreateAccount(self, request, context):
        response_code, message = self.db.insertUser(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)

        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time()
        return response

    def LogIn(self, request, context):
        response_code, message = self.db.logIn(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time()
        return response

    def LogOut(self, request, context):
        response_code, message = self.db.logOut(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time()
        return response

    def DeleteAccount(self, request, context):
        response_code, message = self.db.deleteUser(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time()
        return response

    def GetNewMessages(self, request, context):
        print("Polling Message Stream")
        response_code, messages = self.db.getUndeliveredMessagesForUser(request.sender_id)
        
        if response_code == 201:
            return messages_pb2.RequestMessagesResponse(response_code=response_code, messages=[], error="No New Messages") 
        elif response_code == 404:
            return messages_pb2.RequestMessagesResponse(response_code=response_code, messages=[], error=messages)
        
        pb2MessageList = []
        for msg in messages:
            timestamp = server_utils.timestamp_to_string(msg[5])
            newMessage = messages_pb2.Message(sender_id=msg[1], receiver_id=msg[2], message=msg[3], timestamp = timestamp)
            pb2MessageList.append(newMessage)

        response = messages_pb2.RequestMessagesResponse(response_code=response_code, messages=pb2MessageList, error="")
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.update_time = time.time() 
        return response
        

class Server:

    def sync_with_other_servers(self):
        other_servers = [0,1,2] - self.server_number
        for other in other_servers:
            # connect to other servers
            server_host = config.SERVER_HOSTS[other]
            host = server_host[0]
            port = server_host[1]
            self.channel = grpc.insecure_channel(
                    '{}:{}'.format(host, port))
            stub = server_messages_pb2_grpc.ServerExchangeStub(self.channel)

            clock = ask_for_logical_clock()
            if clock < self.logical_clock:
                db = fetch_db()
                return db

    def start(self):
        self.server_number = int(input("Enter server 1 (0-2): "))
        server_host = config.SERVER_HOSTS[self.server_number]
        port = server_host[1]
        str_port = str(port)


        if (self.server_number == 0):
            db = DB('development.db')
        else:
            #get updated db
            db = self.sync_with_other_servers()


        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        messages_pb2_grpc.add_MessageExchangeServicer_to_server(MessageExchange(db), server)
        server.add_insecure_port('[::]:' + str_port)

        server.start()
        print("Server started, listening on " + str_port)
        server.wait_for_termination()

server = Server()
server.start()
