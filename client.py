import socket
import config
import wire_protocol

def create_client_socket():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((config.SERVER_HOST, config.PORT))
    return clientsocket

def client_options_menu():
    print("Options Menu. Please enter the number of your choice from the following options: ")
    print(" 1. List All Users \n 2. Send Message \n 3. Delete Your Account")

    # capture user input, handling errors
    while True:
        try:
            data=int(input("Enter a Number: "))
            print ("You entered: ", data)
            break;
        except ValueError:
            print ("Invalid input")

    # map user input to request types
    if data == 1:
        return config.LIST_ACCOUNTS
    if data == 2:
        return config.SEND_MESSAGE
    if data == 3:
        return config.ACCOUNT_DELETION
    else:
        print("Invalid input")
        return 
    
def input_message():
    return str(input("Message to Send: "))

def client_main():
    clientsocket = create_client_socket()
    try:
        user_msg = input_message()
        bmsg = wire_protocol.marshal(user_msg)
        sent = clientsocket.send(bmsg)
        
        print('Message sent, %d/%d bytes transmitted' % (sent, len(user_msg)))
        clientsocket.close()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        clientsocket.close()

client_main()