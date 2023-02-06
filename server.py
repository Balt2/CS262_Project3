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