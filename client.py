import datetime
import socket
import string
import config
import wire_protocol
import _thread

class Client:
    def __init__(self):
        self.logged_in_user = None
        self.clientsocket = self.create_client_socket()
        self.client_main()
        _thread.start_new_thread(self.listen_to_server, ())
        #self.listen_to_server()
        
        
    def create_client_socket(self):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((config.SERVER_HOST, config.PORT))
        return clientsocket

    def client_options_menu(self):
        # print the options menu
        print("\n\n----- Options Menu: please enter the number of your choice from the following options. ----- ")
        menu_str = " 1. Create an account \n 2. Log in \n 3. List Accounts \n"
        if self.logged_in_user:
            menu_str += " 4. Send a message \n 5. See your messages \n 6. Delete your account \n 7. Log out \n"
        else:
            menu_str += " 4-7: (must log in to see) \n"
        menu_str += " 8. Exit"
        print(menu_str)

        # capture user input, handling errors
        while True:
            try:
                data=int(input("Enter a Number: "))
                print ("You entered: ", data)

                # map user input to request types
                if data == 1:
                    return config.ACCOUNT_CREATION
                if data == 2:
                    return config.LOG_IN
                if data == 3:
                    return config.LIST_ACCOUNTS
                if data == 4:
                    return config.SEND_MESSAGE
                if data == 5:
                    return config.RECEIVE_MESSAGE
                if data == 6:
                    return config.ACCOUNT_DELETION
                if data == 7:
                    return config.LOG_OUT
                if data == 8:
                    return config.END_SESSION
                else:
                    print("Invalid input")
            except ValueError:
                print ("Invalid input")

    def create_account(self):
        print("create account")
        username = str(input("Username: "))
        return wire_protocol.marshal_request(config.ACCOUNT_CREATION, username, -1, -1)

    def log_in(self):
        print("log in")
        username = str(input("Username: "))
        return wire_protocol.marshal_request(config.LOG_IN, username, -1, -1)

    def send_message(self, sender_id: string="-1"):
        print("send_message")
        user_msg = str(input("Message to Send: "))
        receiver_id = str(input("Recipient username: "))
        return wire_protocol.marshal_request(config.SEND_MESSAGE, sender_id, receiver_id, user_msg)

    def request_messages(self, sender_id: string="-1"):
        print("request messages")
        user_msg = str(input("Messages with username: "))
        return wire_protocol.marshal_request(config.RECEIVE_MESSAGE, sender_id, user_msg)

    def list_accounts(self):
        print("list accounts")
        account_str = str(input("Search for accounts (* to see them all): "))
        return wire_protocol.marshal_request(config.LIST_ACCOUNTS, -1, -1, account_str)

    def log_out(self, sender_id: string="-1"):
        print("log out")
        return wire_protocol.marshal_request(config.LOG_OUT, sender_id)

    def delete_account(self, sender_id: string="-1"):
        print("delete_account")
        return wire_protocol.marshal_request(config.ACCOUNT_DELETION, sender_id)

    def end_session(self):
        print("end session")
        return wire_protocol.marshal_request(config.END_SESSION)

    def parse_response(self, user_action, response_code, message):
        if user_action == config.ACCOUNT_CREATION:
            print(message)
        elif user_action == config.LOG_IN:
            if response_code == 200:
                self.logged_in_user = message
                print("Successfully logged in as: ", self.logged_in_user)
            elif response_code == 404:
                print("Error logging in: ", message)
        elif user_action == config.LIST_ACCOUNTS:
            print(message)
        elif user_action == config.SEND_MESSAGE:
            print(message)
        elif user_action == config.RECEIVE_MESSAGE:
            if response_code == 200:
                messageList = eval(message)
                print(messageList)
                for msg in messageList:
                    intTimestamp = int((msg[5]).split(".", 1)[0])
                    timestamp = datetime.datetime.fromtimestamp(intTimestamp).strftime('%Y-%m-%d %H:%M:%S')
                    print( "( " +timestamp + " ) " + msg[1] + " to " + msg[2] + " : " + msg[3])
            elif response_code == 404:
                print("Error retrieving messages: ", message)
                
        elif user_action == config.ACCOUNT_DELETION:
            if response_code == 200:
                print("Successfully deleted account: ", message)
                self.logged_in_user = None
            elif response_code == 404:
                print("Error deleting account: ", message)
        elif user_action == config.LOG_OUT:
            if response_code == 200:
                print("Successfully logged out: ", message)
                self.logged_in_user = None
            elif response_code == 404:
                print("Error logging out: ", message)
        
    def listen_to_server(self, user_action = None):
        while True:
            bdata, addr = self.clientsocket.recvfrom(1024)
            print("Got data while Listening: ", bdata)
            # parse the response
            response = wire_protocol.unmarshal_response(bdata)
            response_code = response['response_code']
            message = response['message']

            # if user_action == config.END_SESSION:
            #     print("Ending session...")
            #     break

            # parse the response and print the result
            self.parse_response(user_action, response_code, message)
            

    def client_main(self):
        print("Starting client...")
        print("Connected.")

        try:
            while True:
                print("Logged In User: ", self.logged_in_user)
                user_action = self.client_options_menu()
                bmsg = b''

                # parse the user input and prepare the payload
                if self.logged_in_user:
                    if user_action == config.LIST_ACCOUNTS:
                        bmsg = self.list_accounts()
                    elif user_action == config.SEND_MESSAGE:
                        bmsg = self.send_message(sender_id=self.logged_in_user)
                    elif user_action == config.RECEIVE_MESSAGE:
                        bmsg = self.request_messages(sender_id=self.logged_in_user)
                    elif user_action == config.ACCOUNT_DELETION:
                        bmsg = self.delete_account(sender_id=self.logged_in_user)
                    elif user_action == config.LOG_OUT:
                        bmsg = self.log_out(sender_id=self.logged_in_user)
                    else:
                        print("Please log out to perform this action.")
                        continue
                else:
                    if user_action == config.ACCOUNT_CREATION:
                        bmsg = self.create_account()
                    elif user_action == config.LOG_IN:
                        bmsg = self.log_in()
                    elif user_action == config.LIST_ACCOUNTS:
                        bmsg = self.list_accounts()
                    elif user_action == config.END_SESSION:
                        bmsg = self.end_session()
                        
                    else:
                        print("Please log in to perform this action.")
                        continue

                # send the payload along the wire
                sent = self.clientsocket.send(bmsg)
                print('Message sent, %d/%d bytes transmitted' % (sent, len(bmsg)))
                bdata, addr = self.clientsocket.recvfrom(1024)

                # parse the response
                response = wire_protocol.unmarshal_response(bdata)
                response_code = response['response_code']
                message = response['message']

                if user_action == config.END_SESSION:
                    print("Ending session...")
                    break

                # parse the response and print the result
                self.parse_response(user_action, response_code, message)
                
                            
            # after loop, close socket
            self.clientsocket.shutdown(socket.SHUT_RDWR)
            self.clientsocket.close()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            self.clientsocket.shutdown(socket.SHUT_RDWR)
            self.clientsocket.close()

client = Client()
