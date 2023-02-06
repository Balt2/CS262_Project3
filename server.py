import socket
HOST = '127.0.0.1'
PORT = 6000
HBSGUEST = '199.94.1.207'
clientIP = '10.228.19.172'
HOST = '10.228.19.141'
#HOST = clientIP

def server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    print("Server up on IP: ", HOST, " and port: ", PORT )
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
