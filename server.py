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


# host = '192.168.0.12' #Server ip
#     port = 4000

#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind((host, port))

#     print("Server Started")
#     while True:
#         data, addr = s.recvfrom(1024)
#         data = data.decode('utf-8')
#         print("Message from: " + str(addr))
#         print("From connected user: " + data)
#         data = data.upper()
#         print("Sending: " + data)
#         s.sendto(data.encode('utf-8'), addr)
#     c.close()