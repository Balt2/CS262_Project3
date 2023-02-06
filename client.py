import socket
import config

def create_client_socket():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((config.SERVER_HOST, config.PORT))
    return clientsocket

def input_message():
    return str(input("Message to Send: "))

def client_main():
    clientsocket = create_client_socket()

    msg = input_message()
    bmsg = msg.encode('ascii')
    sent = clientsocket.send(bmsg)
    
    print('Message sent, %d/%d bytes transmitted' % (sent, len(msg)))
    clientsocket.close()

client_main()