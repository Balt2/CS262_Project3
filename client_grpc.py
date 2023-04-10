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
        self.logged_in_user = None

        # instantiate the channel
        self.stubs = {}
        self.disconnected_servers = set(config.SERVER_HOSTS)
        # for tuple in config.SERVER_HOSTS:
        #     host = tuple[0]
        #     port = tuple[1]

        #     print(host, port)
        #     try:
        #         self.channel = grpc.insecure_channel(
        #             '{}:{}'.format(host, port))
        #         stub = pb2_grpc.MessageExchangeStub(self.channel)
        #         self.stubs[tuple] = stub
                
        #     except:
        #         print("EXCEPTION with host: ", host, " port: ", port)
        #         self.disconnected_servers.add(tuple)
        #         continue
        self.connect_to_down_servers()
        #Logic to handle SIGINT
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.main()

    def connect_to_down_servers(self):
        connected_servers = set()
        for tuple in self.disconnected_servers:
            host = tuple[0]
            port = tuple[1]
            try:
                self.channel = grpc.insecure_channel(
                    '{}:{}'.format(host, port))
                stub = pb2_grpc.MessageExchangeStub(self.channel)
                self.stubs[tuple] = stub
                connected_servers.add(tuple)
            except:
                continue

        self.disconnected_servers = self.disconnected_servers - connected_servers

    def send_exec(self, code):
        self.connect_to_down_servers()
        new_disconnects = set()
        responses = []
        for host_tuple, stub in self.stubs.items():
            #We do try/catch here because we may no longer be connected to a given stub
            try:
                #We need to use exec here because we are dynamically creating the function call
                exec(code)
            except:
                new_disconnects.add(host_tuple)
                continue

            res = locals()['exec_res']
            for r in responses:
                if res == r:
                    return res
            responses.append(res)

        for host_tuple in new_disconnects:
            self.disconnected_servers.add(host_tuple)
            self.stubs.pop(host_tuple)

        if len(responses) > 0:
            return responses[0]
        else:
            print("All servers down or unresponseive")
            return None
        
        
    
    def create_account(self):
        print("create account")
        username = str(input("Username: "))


        got_response = False
        index = 0

        exec_string = """exec_res = stub.CreateAccount(pb2.AccountRequest(name='{}'), timeout = 1)""".format(username)
        response = self.send_exec(exec_string)

        print(response)
        if response.response_code == 200:
            self.logged_in_user = username
            _thread.start_new_thread(self.get_new_message_stream, ())
        elif response.response_code == 404:
            print("Error creating an account: ", response.response_text)

    def log_in(self):
        print("log in")
        username = str(input("Username: "))

        exec_string = """exec_res = stub.LogIn(pb2.AccountRequest(name='{}'), timeout = 1)""".format(username)
        response = self.send_exec(exec_string)

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
        exec_string = """exec_res = stub.SendMessage(pb2.SendMessageRequest(sender_id='{}', receiver_id='{}', message='{}'), timeout = 1)""".format(self.logged_in_user, receiver_id, user_msg)
        response = self.send_exec(exec_string)
        print(response)

    def request_messages(self):
        print("request messages")
        receiver_id = str(input("Messages with username: "))
        exec_string = """exec_res = stub.RequestMessages(pb2.RequestMessagesRequest(sender_id='{}', receiver_id='{}'), timeout = 1)""".format(self.logged_in_user, receiver_id)
        response = self.send_exec(exec_string)
        print(response)


    def list_accounts(self):
        print("list accounts")
        account_str = str(input("Search for accounts (* to see them all): "))

        exec_string = """exec_res = stub.ListAccounts(pb2.ListAccountsRequest(search_pattern='{}'), timeout = 1)""".format(account_str)
        list_accounts_response = self.send_exec(code=exec_string)

        print(list_accounts_response)

    def log_out(self):
        print("log out")
        exec_string = """exec_res = stub.LogOut(pb2.AccountRequest(name='{}'), timeout = 1)""".format(self.logged_in_user)
        response = self.send_exec(code=exec_string)

        if response.response_code == 200:
            self.logged_in_user = None
            print("Logged out successfully")
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def delete_account(self, sender_id: string="-1"):
        print("delete_account")
        exec_string = """exec_res = stub.DeleteAccount(pb2.AccountRequest(name='{}'), timeout = 1)""".format(self.logged_in_user)
        response = self.send_exec(code=exec_string)
        print(response)
        if response.response_code == 200:
            print("Deleted account successfully")
            self.logged_in_user = None
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def get_new_message_stream(self):
        while self.logged_in_user:
            exec_string = """exec_res = stub.GetNewMessages(pb2.GetNewMessagesRequest(sender_id='{}'), timeout = 1)""".format(self.logged_in_user)
            response = self.send_exec(code=exec_string)

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

