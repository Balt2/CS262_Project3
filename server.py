import socket
import config
import re
import wire_protocol
import _thread

from db import DB

    
class Server:
    def __init__(self):
        self.db = DB('development.db')
        self.sockets = {}

    def handleRequest(self, msg, clientsocket):
        try:
            msg_request_type = msg['request_type']
            if msg_request_type == config.ACCOUNT_CREATION:
                print("Creating account...")
                response_code, username = self.db.insertUser(msg['sender_id'])
                
                if response_code == 200:
                    self.sockets[username] = clientsocket
                    print("Created user in client sockets: ", username)
                    print(clientsocket)

                return response_code, username
            elif msg_request_type == config.LOG_IN:
                print("Logging in...")
                response_code, username = self.db.logIn(msg['sender_id'])

                if response_code == 200:
                    self.sockets[username] = clientsocket
                    print("Logged in user in client sockets: ", username)

                return response_code, username
            
            elif msg_request_type == config.LIST_ACCOUNTS:
                print("Listing accounts...")
                search_pattern = msg['message'] or ""
                response_code, accounts = self.db.listAccounts()
                filtered_accounts = []

                # apply the wildcard search to results
                for act in accounts:
                    username = act[0]
                    if search_pattern == "*":
                        filtered_accounts.append(username)
                    elif "*" in search_pattern:
                        index = search_pattern.index('*')
                        if username[0:index] == search_pattern[0:index]:
                            filtered_accounts.append(username)
                    else:
                        if re.match(search_pattern, username):
                            filtered_accounts.append(username)

                return response_code, filtered_accounts

            elif msg_request_type == config.SEND_MESSAGE:
                print("Sending message...")
                response_code, message = self.db.insertMessage(msg['sender_id'], msg['receiver_id'], msg['message'])
                if response_code == 200:
                    print("Message saved to DB! Sending message to recipient...")
                    if msg['receiver_id'] in self.sockets:
                        print("Found recipient socket")
                        self.sockets[msg['receiver_id']].send(wire_protocol.marshal_response(config.RECEIVE_MESSAGE, 200, (msg['message'], msg['sender_id'])))
                    else:
                        print("Recipient not logged in")

                return response_code, message
            
            elif msg_request_type == config.REQUEST_MESSAGES:
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
                try:

                    socket_list = list(self.sockets.values())
                    socket_index = socket_list.index(clientsocket)
                   
                    if (socket_list[socket_index].getpeername() == clientsocket.getpeername()):
                        username = list(self.sockets.keys())[socket_index]
                        print("Socket found in list of sockets. Removing and logging out user...".format(username))
                        response_code, username = self.db.logOut(username)
                        self.sockets.pop(username)

                    
                    return 502, username
                except:
                    return 502, "User was not logged in. Socket was disconnected."

        
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

            response_code, response_payload = self.handleRequest(msg, clientsocket)
            if response_code == 502:
                print("Client disconnected: {} ".format(response_payload), client_addr)
                clientsocket.close()
                break

            msg_request_type = msg['request_type']
            response = wire_protocol.marshal_response(msg_request_type, response_code, response_payload)
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
                #Start new thread for each client
                _thread.start_new_thread(self.listen_to_client, (clientsocket, client_addr))
    
    #TODO: Signout all users when the server is shut down
    def stop(self):
        print("Server shutting down...")
        for username in self.sockets.keys():
            self.db.logOut(username)


server = Server()
server.start()


