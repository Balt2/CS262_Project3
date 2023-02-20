import sys
from concurrent import futures
sys.path.append('../../CS262_Project1')

import config
from db import DB
import grpc
import messages_pb2
import messages_pb2_grpc

class MessageExchange(messages_pb2_grpc.MessageExchange):
    def __init__(self):
        self.db = DB('../test3.db')
    
    def ListAccounts(self, request, context):
        response_code, accounts = self.db.listAccounts()
        response = messages_pb2.ListAccountsResponse()
        for act in accounts:
            account_obj = messages_pb2.Account(name=act[0])
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
