import datetime
import sys
from concurrent import futures
sys.path.append('../CS262_Project1')

import config
from db import DB
import grpc
import messages_pb2
import messages_pb2_grpc
import server_utils

class MessageExchange(messages_pb2_grpc.MessageExchange):
    def __init__(self):
        self.db = DB('../development.db')
    
    def ListAccounts(self, request, context):
        response_code, accounts = self.db.listAccounts()
        response = messages_pb2.ListAccountsResponse()
        search_pattern = request.search_pattern
        for act in accounts:
            username = act[0]
            if server_utils.should_include_account(username, search_pattern):
                account_obj = messages_pb2.Account(name=username)
                response.accounts.append(account_obj)

        return response

    def SendMessage(self, request, context):
        response_code, delivered = self.db.insertMessage(
            request.sender_id,
            request.receiver_id,
            request.message
        )
        
        response = messages_pb2.SendMessageResponse(response_code=response_code, delivered=delivered)
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
        return response

    def CreateAccount(self, request, context):
        response_code, message = self.db.insertUser(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        return response

    def LogIn(self, request, context):
        response_code, message = self.db.logIn(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        return response

    def LogOut(self, request, context):
        response_code, message = self.db.logOut(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
        return response

    def DeleteAccount(self, request, context):
        response_code, message = self.db.deleteUser(request.name)
        response = messages_pb2.AccountResponse(response_code=response_code, response_text=message)
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
        return response
        

class Server:
    def start(self):
        str_port = str(config.GRPC_PORT)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        messages_pb2_grpc.add_MessageExchangeServicer_to_server(MessageExchange(), server)
        server.add_insecure_port('[::]:' + str_port)

        server.start()
        print("Server started, listening on " + str_port)
        server.wait_for_termination()

server = Server()
server.start()
