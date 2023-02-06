import socket
import config

def server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((config.SERVER_HOST, config.PORT))
    print("Server up on IP: ", config.SERVER_HOST, " and port: ", config.PORT )
    while True:
        print('server listening...')
        serversocket.listen()
        clientsocket, client_addr = serversocket.accept()
        bdata, addr = clientsocket.recvfrom(1024)
        data = bdata.decode('ascii')
        print("Data from Client Socket: ", clientsocket)
        print("Got Data: ", data, " from Address: ", client_addr)

        
    serversocket.close()

server()
