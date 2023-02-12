import socket
import config
import wire_protocol

def create_client_socket():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((config.SERVER_HOST, config.PORT))
    return clientsocket

def client_options_menu():
    print("\n\n----- Options Menu: please enter the number of your choice from the following options. ----- ")
    print(" 1. Create an account \n 2. List Accounts \n 3. Send a message \n 4. Delete your account \n 5. Exit ")

    # capture user input, handling errors
    while True:
        try:
            data=int(input("Enter a Number: "))
            print ("You entered: ", data)

            # map user input to request types
            if data == 1:
                return config.ACCOUNT_CREATION
            if data == 2:
                return config.LIST_ACCOUNTS
            if data == 3:
                return config.SEND_MESSAGE
            if data == 4:
                return config.ACCOUNT_DELETION
            if data == 5:
                return config.END_SESSION
            else:
                print("Invalid input")
        except ValueError:
            print ("Invalid input")
    
def create_account():
    print("create account")
    username = str(input("Username: "))
    return wire_protocol.marshal(config.ACCOUNT_CREATION, username, -1, -1)
    

def send_message():
    print("send_message")
    user_msg = str(input("Message to Send: "))
    # TODO: figure out receiver and sender id
    return wire_protocol.marshal(config.SEND_MESSAGE, 1, -1, user_msg)

def list_accounts():
    print("list accounts")
    # TODO: figure out sender id
    return wire_protocol.marshal(config.LIST_ACCOUNTS, 1)
    

def delete_account():
    print("delete_account")
    # TODO: figure out sender id
    return wire_protocol.marshal(config.ACCOUNT_DELETION, 1)

def client_main():
    print("Starting client...")
    clientsocket = create_client_socket()
    print("Connected.")

    try:
        while True:
            user_action = client_options_menu()

            bmsg = b''
            if user_action == config.ACCOUNT_CREATION:
                bmsg = create_account()
            elif user_action == config.LIST_ACCOUNTS:
                bmsg = list_accounts()
            elif user_action == config.SEND_MESSAGE:
                bmsg = send_message()
            elif user_action == config.ACCOUNT_DELETION:
                bmsg = delete_account()
            elif user_action == config.END_SESSION:
                break;
            
            # match user_action:
            #     case config.ACCOUNT_CREATION:
            #         bmsg = create_account()

            #     case config.LIST_ACCOUNTS:
            #         bmsg = list_accounts()

            #     case config.SEND_MESSAGE:
            #         bmsg = send_message()

            #     case config.ACCOUNT_DELETION:
            #         bmsg = delete_account()

            #     case config.END_SESSION:
            #         break;
            

            sent = clientsocket.send(bmsg)
            print('Message sent, %d/%d bytes transmitted' % (sent, len(bmsg)))
    
        # after loop, close socket
        clientsocket.close()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        clientsocket.close()

client_main()