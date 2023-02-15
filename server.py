import socket
import config
import re
import wire_protocol
import _thread

from db import DB

class ClientSocket:
    def __init__(self, clientsocket, client_addr, db):
        self.clientsocket = clientsocket
        self.client_addr = client_addr
        self.db = db
        
    
    def listen(self):
        while True:
            bdata, addr = self.clientsocket.recvfrom(1024)
            print("Data from Client Socket: ", self.clientsocket)
            print("BDATA: ", bdata)
            msg = wire_protocol.unmarshal_request(bdata)
            print("Got MSSG: ", msg, " from Address: ", self.client_addr)
            response_code, response_payload = handleRequest(msg, self.db)
            response = wire_protocol.marshal_response(response_code, response_payload)
            sent = self.clientsocket.send(response)
            print('Server responded, %d/%d bytes transmitted' % (sent, len(response)))

        self.clientsocket.close()
    
    def send(self, bmsg):
        self.clientsocket.send(bmsg)

    def close(self):
        self.clientsocket.close()

def handleRequest(msg, db):
    try:
        msg_request_type = msg['request_type']
        if msg_request_type == config.ACCOUNT_CREATION:
            print("Creating account...")
            return db.insertUser(msg['sender_id'])
        elif msg_request_type == config.LOG_IN:
            print("Logging in...")
            return db.logIn(msg['sender_id'])
        elif msg_request_type == config.LIST_ACCOUNTS:
            print("Listing accounts...")
            search_pattern = msg['message']
            print("search_pattern =", search_pattern)
            response_code, accounts = db.listAccounts()
            print("accounts! = ", accounts)
            # filtered_accounts = (lambda: a: a[0], accounts)
            # print("filtered_accounts! = ", filtered_accounts)
            return response_code, accounts
        elif msg_request_type == config.SEND_MESSAGE:
            print("Sending message...")
            return db.insertMessage(msg['sender_id'], msg['receiver_id'], msg['message'])
        elif msg_request_type == config.RECEIVE_MESSAGE:
            print("Receiving message...")
            return db.getMessagesForChat(msg['sender_id'], msg['receiver_id'])
        elif msg_request_type == config.ACCOUNT_DELETION:
            print("Deleting account...")
            return db.deleteUser(msg['sender_id'])
        elif msg_request_type == config.LOG_OUT:
            print("Logging Out...")
            return db.logOut(msg['sender_id'])
        elif msg_request_type == config.END_SESSION:
            print("Ending session...")
            #TODO: Remove socket from list of sockets
            return 200, ""
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return 404, ""
    
    print("ERROR: Request type not found...")
    return 404, "request type not found"
    
def server():
    #Helpful https://realpython.com/python-sockets/
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((config.SERVER_HOST, config.PORT))
        print("Server up on IP: ", config.SERVER_HOST, " and port: ", config.PORT )

        #Create DB Object
        db = DB('test.db')
        print("Server loaded DB: ")
        
        s.listen()
        print("Server listening...")
        while True:
            clientsocket, client_addr = s.accept()
            newClient = ClientSocket(clientsocket, client_addr, db)
            _thread.start_new_thread(newClient.listen, ())
            
            # with clientsocket:
            #     print('Connected by', client_addr)
            #     while True:
            #         bdata, addr = clientsocket.recvfrom(1024)
            #         print("Data from Client Socket: ", clientsocket)
            #         print("BDATA: ", bdata)
            #         msg = wire_protocol.unmarshal_request(bdata)
            #         print("Got MSSG: ", msg, " from Address: ", client_addr)

            #         response_code, response_payload = handleRequest(msg, db)
                    
            #         response = wire_protocol.marshal_response(response_code, response_payload)
            #         sent = clientsocket.send(response)
            #         print('Server responded, %d/%d bytes transmitted' % (sent, len(response)))


server()

