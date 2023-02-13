import socket
import string
import config
import wire_protocol

def create_client_socket():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((config.SERVER_HOST, config.PORT))
    return clientsocket

def client_options_menu(logged_in_user):
    # print the options menu
    print("\n\n----- Options Menu: please enter the number of your choice from the following options. ----- ")
    menu_str = " 1. Create an account \n 2. Log in \n 3. List Accounts \n"
    if logged_in_user:
        menu_str += " 4. Send a message \n 5. See your messages \n 6. Delete your account \n 7. Log out \n"
    else:
        menu_str += " 4-7: (must log in to see)  \n"
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

def create_account():
    print("create account")
    username = str(input("Username: "))
    return wire_protocol.marshal(config.ACCOUNT_CREATION, username, -1, -1)

def log_in():
    print("log in")
    username = str(input("Username: "))
    return wire_protocol.marshal(config.LOG_IN, username, -1, -1)

def send_message(sender_id: string="-1"):
    print("send_message")
    user_msg = str(input("Message to Send: "))
    receiver_id = str(input("Recipient username: "))
    return wire_protocol.marshal(config.SEND_MESSAGE, sender_id, receiver_id, user_msg)

def request_messages(sender_id: string="-1"):
    print("request messages")
    return wire_protocol.marshal(config.RECEIVE_MESSAGE, sender_id)

def list_accounts():
    print("list accounts")
    return wire_protocol.marshal(config.LIST_ACCOUNTS)

def log_out(sender_id: string="-1"):
    print("log out")
    return wire_protocol.marshal(config.LOG_OUT, sender_id)

def delete_account(sender_id: string="-1"):
    print("delete_account")
    return wire_protocol.marshal(config.ACCOUNT_DELETION, sender_id)

def end_session():
    print("end session")
    return wire_protocol.marshal(config.END_SESSION)

def client_main():
    print("Starting client...")
    clientsocket = create_client_socket()
    print("Connected.")
    logged_in_user = None

    try:
        while True:
            print("Logged In User: ", logged_in_user)
            user_action = client_options_menu(logged_in_user)
            bmsg = b''

            # parse the user input and prepare the payload
            if logged_in_user:
                if user_action == config.LIST_ACCOUNTS:
                    bmsg = list_accounts()
                elif user_action == config.SEND_MESSAGE:
                    bmsg = send_message(sender_id=logged_in_user)
                elif user_action == config.RECEIVE_MESSAGE:
                    bmsg = request_messages(sender_id=logged_in_user)
                elif user_action == config.ACCOUNT_DELETION:
                    bmsg = delete_account(sender_id=logged_in_user)
                elif user_action == config.LOG_OUT:
                    bmsg = log_out(sender_id=logged_in_user)
                else:
                    print("Please log out to perform this action.")
                    continue
            else:
                if user_action == config.ACCOUNT_CREATION:
                    bmsg = create_account()
                elif user_action == config.LOG_IN:
                    bmsg = log_in()
                elif user_action == config.LIST_ACCOUNTS:
                    bmsg = list_accounts()
                elif user_action == config.END_SESSION:
                    bmsg = end_session()
                    
                else:
                    print("Please log in to perform this action.")
                    continue

            # send the payload along the wire
            sent = clientsocket.send(bmsg)
            print('Message sent, %d/%d bytes transmitted' % (sent, len(bmsg)))
            bdata, addr = clientsocket.recvfrom(1024)

            # parse the response
            msg_response = wire_protocol.unmarshal(bdata)
            print('!!!! msg_response: ', msg_response)
            print('Message received: ', msg_response['message'])
            message = eval(msg_response['message'])
            print("message = ", message)

            if user_action == config.ACCOUNT_CREATION:
                print(message)
            elif user_action == config.LOG_IN:
                if message[0] == 200:
                    logged_in_user = message[1]
                    print("Successfully logged in as: ", logged_in_user)
                elif message[0] == 404:
                    print("Error logging in: ", message[1])
            elif user_action == config.LIST_ACCOUNTS:
                print(message)
            elif user_action == config.SEND_MESSAGE:
                print(message)
            elif user_action == config.RECEIVE_MESSAGE:
                print(message)
            elif user_action == config.ACCOUNT_DELETION:
                if message[0] == 200:
                    print("Successfully deleted account: ", message[1])
                    logged_in_user = None
                elif message[0] == 404:
                    print("Error deleting account: ", message[1])

            elif user_action == config.LOG_OUT:
                if message[0] == 200:
                    print("Successfully logged out: ", message[1])
                    logged_in_user = None
                elif message[0] == 404:
                    print("Error logging out: ", message[1])
            elif user_action == config.END_SESSION:
                print("Ending session...")
                break
                        
        # after loop, close socket
        clientsocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        clientsocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()

client_main()