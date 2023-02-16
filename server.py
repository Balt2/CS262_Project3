import socket
import config
import re
import wire_protocol
import _thread

from db import DB

    
class Server:
    def __init__(self):
        self.db = DB('test3.db')
        self.sockets = {}

    def handleRequest(self, msg, client_addr, clientsocket):
        try:
            msg_request_type = msg['request_type']
            if msg_request_type == config.ACCOUNT_CREATION:
                print("Creating account...")
                return self.db.insertUser(msg['sender_id'])
            elif msg_request_type == config.LOG_IN:
                print("Logging in...")
                response_code, username = self.db.logIn(msg['sender_id'])

                if response_code == 200:
                    self.sockets[username] = clientsocket
                    print("Logged in user in client sockets: ", username)

                return response_code, username
            
            elif msg_request_type == config.LIST_ACCOUNTS:
                print("Listing accounts...")
                search_pattern = msg['message']
                print("search_pattern =", search_pattern)
                response_code, accounts = self.db.listAccounts()
                print("accounts! = ", accounts)
                # filtered_accounts = (lambda: a: a[0], accounts)
                # print("filtered_accounts! = ", filtered_accounts)
                return response_code, accounts
            elif msg_request_type == config.SEND_MESSAGE:
                print("Sending message...")
                response_code, message = self.db.insertMessage(msg['sender_id'], msg['receiver_id'], msg['message'])
                if response_code == 200:
                    print("Message saved to DB!")
                    print("Sending message to recipient...")
                    if msg['receiver_id'] in self.sockets:
                        print("Found recipient socket")
                        self.sockets[msg['receiver_id']].send(wire_protocol.marshal_response(200, (msg['sender_id'], msg['message'])))
                    else:
                        print("Recipient not logged in")

                return response_code, message
            
            elif msg_request_type == config.RECEIVE_MESSAGE:
                print("Receiving message...")
                return self.db.getMessagesForChat(msg['sender_id'], msg['receiver_id'])
            elif msg_request_type == config.ACCOUNT_DELETION:
                print("Deleting account...")
                return self.db.deleteUser(msg['sender_id'])
            elif msg_request_type == config.LOG_OUT:
                
                print("Logging Out...")
                response_code, username = self.db.logOut(msg['sender_id'])

                if response_code == 200:
                    self.sockets.pop(username)
                    print("Logged out user: ", username)

                return response_code, username
            
            elif msg_request_type == config.END_SESSION:
                print("Ending session...")
                return 200, ""
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return 404, ""
        
        print("ERROR: Request type not found...")
        return 404, "request type not found"
    
    def listen_to_client(self, clientsocket, client_addr):
        
        while True:
            bdata, addr = clientsocket.recvfrom(1024)
            print("Data from Client Socket: ", clientsocket)
            msg = wire_protocol.unmarshal_request(bdata)
            print("Got MSSG: ", msg, " from Address: ", client_addr)

            response_code, response_payload = self.handleRequest(msg, client_addr, clientsocket)
            
            response = wire_protocol.marshal_response(msg['request_type'], response_code, response_payload)
            sent = clientsocket.send(response)
            print('Server responded, %d/%d bytes transmitted' % (sent, len(response)))
            

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((config.SERVER_HOST, config.PORT))
            print("Server up on IP: ", config.SERVER_HOST, " and port: ", config.PORT )

            s.listen()
            print("Server listening...")
            while True:
                clientsocket, client_addr = s.accept()
                print("Client connected: ", client_addr)
                print("Client IP: ", client_addr[0], " Client Port: ", client_addr[1])
                _thread.start_new_thread(self.listen_to_client, (clientsocket, client_addr))
                # self.sockets.append(newClient)

server = Server()
server.start()

