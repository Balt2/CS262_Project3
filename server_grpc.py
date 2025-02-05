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
    def __init__(self, db, logical_clock):
        self.db = db
        self.logical_clock = logical_clock
        print("Server Exchange Init")

    def SyncDB(self, request, context):
        print("SYNC DB")
        response = server_messages_pb2.SyncDBResponse()
        _, accounts = self.db.listAccounts()
        for account in accounts:
            account_obj = server_messages_pb2.DBAccount(username=account[0], logged_in=account[1], created_at=account[2])
            response.db_accounts.append(account_obj)

        print("Accounts: ", accounts)
        _, messages = self.db.listMessages()
        for message in messages:
            message_obj = server_messages_pb2.DBMessage(id=message[0], sender_id=message[1], receiver_id=message[2], content=message[3], delivered=message[4], created_at=message[5])
            response.db_messages.append(message_obj)
        
        print("Messages: ", messages)
        #response.db_accounts 
        return response
    
    def GetLogicalClock(self, request, context):
        print("GET LOGICAL CLOCK")
        response = server_messages_pb2.GetLogicalClockResponse()
        
        response.logical_clock = self.logical_clock.clock

        return response

class LogicalClock():
    def __init__(self):
        self.clock = 0
    
    def increment(self):
        self.clock += 1


class MessageExchange(messages_pb2_grpc.MessageExchange):
    def __init__(self, db, logical_clock):
        self.db = db
        self.logical_clock = logical_clock

    
    def ListAccounts(self, request, context):
        response_code, accounts = self.db.listAccounts()
        response = messages_pb2.ListAccountsResponse()
        response.response_code = response_code
        search_pattern = request.search_pattern
        for act in accounts:
            username = act[0]
            if server_utils.should_include_account(username, search_pattern):
                account_obj = messages_pb2.Account(name=username)
                response.accounts.append(account_obj)

        #Update the last time the server responded (used for polling/as a heartbeat)
        self.logical_clock.increment()

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
        self.logical_clock.increment()
        
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
        self.logical_clock.increment()
        return response

    def CreateAccount(self, request, context):
        response_code, message = self.db.insertUser(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)

        #Update the last time the server responded (used for polling/as a heartbeat)
        self.logical_clock.increment()
        return response

    def LogIn(self, request, context):
        response_code, message = self.db.logIn(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.logical_clock.increment()
        return response

    def LogOut(self, request, context):
        response_code, message = self.db.logOut(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.logical_clock.increment()
        return response

    def DeleteAccount(self, request, context):
        response_code, message = self.db.deleteUser(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        #Update the last time the server responded (used for polling/as a heartbeat)
        self.logical_clock.increment()
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
        self.logical_clock.increment()
        return response
        

class Server:

    def sync_with_other_servers(self):
        other_servers = set([0,1,2]) - set([self.server_number])
        other_server_stubs = {}
        max_logical_clock = (-1, 0) #(logical_clock, server_number)
        for other in other_servers:

            # connect to other servers
            server_host = config.SERVER_HOSTS[other]
            host = server_host[0]
            port = server_host[1]
            print(server_host)
            try:
                self.channel = grpc.insecure_channel(
                    '{}:{}'.format(host, port))
                print("CHANNEL: ", self.channel)
                stub = server_messages_pb2_grpc.ServerExchangeStub(self.channel)
                
                response = stub.GetLogicalClock(server_messages_pb2.GetLogicalClockRequest(), timeout=1)
                print("LOGICAL CLOCK: ", response.logical_clock)
                if response.logical_clock > max_logical_clock[0]:
                    max_logical_clock = (response.logical_clock, other)
                other_server_stubs[other] = stub                
            except:
                print("EXCEPTION")
                continue
        
        #IF unable to connect to any other servers, return local db
        if max_logical_clock[0] == -1 or other_server_stubs == {}:
            return DB("{}-db".format(self.server_number))
        
        # get db from server with max logical clock
        latest_stub = other_server_stubs[max_logical_clock[1]]
        response = latest_stub.SyncDB(server_messages_pb2.SyncDBRequest())
        db = DB("{}-db".format(self.server_number))

        db.wipeDBEntries()
        
        db.forceInsertListOfAccounts(response.db_accounts)
        db.forceInsertListOfMessages(response.db_messages)
        print("SERVER ALL CAUGHT UP")
        return db

        
    def start(self):
        self.logical_clock = 0
        self.server_number = int(input("Enter server 1 (0-2): "))
        server_host = config.SERVER_HOSTS[self.server_number]
        server_port = server_host[1]

        self.logical_clock = LogicalClock()


        # get updated db from peers
        db = self.sync_with_other_servers()



        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        server_messages_pb2_grpc.add_ServerExchangeServicer_to_server(ServerExchange(db, self.logical_clock), server)
        messages_pb2_grpc.add_MessageExchangeServicer_to_server(MessageExchange(db, self.logical_clock), server)

        server.add_insecure_port('[::]:' + str(server_port))

        server.start()
        print("Server started, listening on " + str(server_port))
        
        server.wait_for_termination()

server = Server()
server.start()
