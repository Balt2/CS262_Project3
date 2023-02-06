import socket
# INTERNAL_HOST = '127.0.0.1'
HOST = '10.228.19.172'
BEN_HOST = '10.228.19.141'
PORT = 6000

def create_client_socket():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((BEN_HOST, PORT))
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