import datetime
import socket
import string
import config
import sqlite3

from db import DB

def server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((config.SERVER_HOST, config.PORT))
    print("Server up on IP: ", config.SERVER_HOST, " and port: ", config.PORT )
    db = DB('test.db')
    print("Server loaded DB: ")

    while True:
        print('server listening...')
        db.printTable("accounts")
        serversocket.listen()
        clientsocket, client_addr = serversocket.accept()
        bdata, addr = clientsocket.recvfrom(1024)
        data = bdata.decode('ascii')
        print("Data from Client Socket: ", clientsocket)
        print("Got Data: ", data, " from Address: ", client_addr)

        
    serversocket.close()


server()

