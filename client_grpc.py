import _thread
import time

import client_utils
import config
import grpc
import messages_pb2 as pb2
import messages_pb2_grpc as pb2_grpc
import string
import signal

class GrpcClient():

    def __init__(self):
        self.hosts = config.SERVER_HOSTS
        self.ports = config.GRPC_PORTS

        self.logged_in_user = None

        # instantiate the channel
        self.stubs = []
        for i in range(len(self.ports)):
            try:
                self.channel = grpc.insecure_channel(
                    '{}:{}'.format(self.hosts[i], config.GRPC_PORT))
                stub = pb2_grpc.MessageExchangeStub(self.channel)
                self.stubs.append(stub)
            except:
                continue

        # self.channel = grpc.insecure_channel(
        #     '{}:{}'.format(self.host, self.port))
        
        # self.stub = pb2_grpc.MessageExchangeStub(self.channel)

        # self.channel_2 = grpc.insecure_channel(
        #     '{}:{}'.format(self.host, self.port_2))
        # self.stub = pb2_grpc.MessageExchangeStub(self.channel_2)

        #Logic to handle SIGINT
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.main()

    
    def send_to_all_stubs(self, request):
        for stub in self.stubs:
            try:
                response = stub.SendMessage(request)
                return response
            except:
                continue
     
    def send_exec(self, code):
        got_response = False
        index = 0
        response = None
        for stub in self.stubs:
            print(code)
            res = exec(code)
            print(res)
            if res.response_code == 200 and not got_response:
                response = res
                got_response = True
            elif index == len(self.stubs) - 1 and not got_response:
                response = res
            index += 1    
                
            
        return response
    
    def create_account(self):
        print("create account")
        username = str(input("Username: "))


        got_response = False
        index = 0

        # exec_string = "stub.CreateAccount(pb2.AccountRequest(name='{}'))".format(username)
        # #param1 = pb2.AccountRequest(name=username)
        # response = self.send_exec(code=exec_string)

        for stub in self.stubs:
            res = stub.CreateAccount(pb2.AccountRequest(name=username))
            if res.response_code == 200 and not got_response:
                response = res
                got_response = True
            elif index == len(self.stubs) - 1 and not got_response:
                response = res
            index += 1

        print(response)
        if response.response_code == 200:
            self.logged_in_user = username
            _thread.start_new_thread(self.get_new_message_stream, ())
        elif response.response_code == 404:
            print("Error creating an account: ", response.response_text)

    def log_in(self):
        print("log in")
        username = str(input("Username: "))


        for stub in self.stubs:
            response = stub.LogIn(pb2.AccountRequest(name=username))


        print(response)
        if response.response_code == 200:
            self.logged_in_user = username
            _thread.start_new_thread(self.get_new_message_stream, ())

        elif response.response_code == 404:
            print("Error logging in: ", response.response_text)

    def send_message(self, sender_id: string="-1"):
        print("send_message")
        user_msg = str(input("Message to Send: "))
        receiver_id = str(input("Receiver username: "))
        for stub in self.stubs:
            send_message_response = stub.SendMessage(
                pb2.SendMessageRequest(
                    sender_id=self.logged_in_user,
                    receiver_id=receiver_id,
                    message=user_msg
                )
            )
        print(send_message_response)

    def request_messages(self):
        print("request messages")
        receiver_id = str(input("Messages with username: "))
        for stub in self.stubs:
            request_messages_response = stub.RequestMessages(
                pb2.RequestMessagesRequest(
                    sender_id=self.logged_in_user,
                    receiver_id=receiver_id
                )
            )
        print(request_messages_response)

    def list_accounts(self):
        print("list accounts")
        account_str = str(input("Search for accounts (* to see them all): "))
        for stub in self.stubs:
            try:
                list_accounts_response = stub.ListAccounts(pb2.ListAccountsRequest(search_pattern=account_str))
            except:
                continue

        print(list_accounts_response)

    def log_out(self):
        print("log out")
        for stub in self.stubs:
            response = stub.LogOut(pb2.AccountRequest(name=self.logged_in_user))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = None
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def delete_account(self, sender_id: string="-1"):
        print("delete_account")
        for stub in self.stubs:
            response = stub.DeleteAccount(pb2.AccountRequest(name=self.logged_in_user))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = None
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def get_new_message_stream(self):
        while self.logged_in_user:
            for stub in self.stubs:
                response = stub.GetNewMessages(pb2.GetNewMessagesRequest(sender_id=self.logged_in_user))

            if response.response_code == 200:
                print("New Messages: ", response)
                print("Press enter to continue...")

            #How long we wait to poll the server for new messages  
            time.sleep(1)

        return

    def end_session(self):
        if self.logged_in_user:
            self.log_out()


    def signal_handler(self, signal, frame):
        
        print('You quit the program!')
        self.end_session()
        self.SIGINT = True
        sys.exit(0)

    def main(self):
        print("Starting client...")

        try:
            while True:
                print("Logged In User: ", self.logged_in_user)
                user_action = client_utils.client_options_menu(self.logged_in_user)
                
                # parse the user input and prepare the payload
                if self.logged_in_user:
                    if user_action == config.LIST_ACCOUNTS:
                        self.list_accounts()
                    elif user_action == config.SEND_MESSAGE:
                        self.send_message()
                    elif user_action == config.REQUEST_MESSAGES:
                        self.request_messages()
                    elif user_action == config.ACCOUNT_DELETION:
                        self.delete_account()
                    elif user_action == config.LOG_OUT:
                        self.log_out()
                    else:
                        if (user_action == config.ERROR):
                            continue
                        else:
                            print("Please log out to perform this action.")
                            continue
                else:
                    if user_action == config.ACCOUNT_CREATION:
                        self.create_account()
                    elif user_action == config.LOG_IN:
                        self.log_in()
                    elif user_action == config.LIST_ACCOUNTS:
                        self.list_accounts()
                    elif user_action == config.END_SESSION:
                        self.end_session()
                        
                    else:
                        if (user_action == config.ERROR):
                            continue
                        else:
                            print("Please log in to perform this action.")
                            continue

                if user_action == config.END_SESSION:
                    print("Ending session...")
                    break

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")



client = GrpcClient()

#Used if the user presses Ctrl+C

