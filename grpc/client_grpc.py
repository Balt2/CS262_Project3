import sys
sys.path.append('../../CS262_Project1')

import config
import grpc
import messages_pb2 as pb2
import messages_pb2_grpc as pb2_grpc
import string

class GrpcClient():

    def __init__(self):
        self.host = config.SERVER_HOST
        self.port = config.GRPC_PORT
        self.logged_in_user = None

        # instantiate the channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.port))
        
        self.stub = pb2_grpc.MessageExchangeStub(self.channel)

        self.main()

    def create_account(self):
        print("create account")
        username = str(input("Username: "))
        response = self.stub.CreateAccount(pb2.AccountRequest(name=username))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = username
        elif response.response_code == 404:
            print("Error creating an account: ", response.response_text)

    def log_in(self):
        print("log in")
        username = str(input("Username: "))
        response = self.stub.LogIn(pb2.AccountRequest(name=username))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = username
        elif response.response_code == 404:
            print("Error logging in: ", response.response_text)

    def send_message(self, sender_id: string="-1"):
        print("send_message")
        # TODO

    def request_messages(self, sender_id: string="-1"):
        print("request messages")
        # TODO

    def list_accounts(self):
        print("list accounts")
        list_accounts_response = self.stub.ListAccounts(pb2.ListAccountsRequest())
        print(list_accounts_response)

    def log_out(self):
        print("log out")
        response = self.stub.LogOut(pb2.AccountRequest(name=self.logged_in_user))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = None
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def delete_account(self, sender_id: string="-1"):
        print("delete_account")
        response = self.stub.DeleteAccount(pb2.AccountRequest(name=self.logged_in_user))
        print(response)
        if response.response_code == 200:
            self.logged_in_user = None
        elif response.response_code == 404:
            print("Error logging out: ", response.response_text)

    def end_session(self):
        print("end session")

    # same as the function from the other client.py file, can consolidate
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


    def main(self):
        print("Starting client...")

        try:
            while True:
                print("Logged In User: ", self.logged_in_user)
                user_action = self.client_options_menu()
                
                # parse the user input and prepare the payload
                if self.logged_in_user:
                    if user_action == config.LIST_ACCOUNTS:
                        self.list_accounts()
                    elif user_action == config.SEND_MESSAGE:
                        self.send_message()
                    elif user_action == config.RECEIVE_MESSAGE:
                        self.request_messages()
                    elif user_action == config.ACCOUNT_DELETION:
                        self.delete_account()
                    elif user_action == config.LOG_OUT:
                        self.log_out()
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
                        print("Please log in to perform this action.")
                        continue

                if user_action == config.END_SESSION:
                    print("Ending session...")
                    break

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")



client = GrpcClient()
