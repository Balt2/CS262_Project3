import socket
import config
import wire_protocol

from db import DB

def handleRequest(msg, db):
    msg_request_type = msg['request_type']
    if msg_request_type == config.ACCOUNT_CREATION:
        print("Creating account...")
        return db.insertUser(msg['sender_id'])
    elif msg_request_type == config.LOG_IN:
        print("Logging in...")
        return db.logIn(msg['sender_id'])
    elif msg_request_type == config.LIST_ACCOUNTS:
        print("Listing accounts...")
        return db.listAccounts()
        
    elif msg_request_type == config.SEND_MESSAGE:
        print("Sending message...")
        return db.insertMessage(msg['sender_id'], msg['receiver_id'], msg['message'])
    elif msg_request_type == config.ACCOUNT_DELETION:
        print("Deleting account...")
        return db.deleteUser(msg['sender_id'])
    elif msg_request_type == config.LOG_OUT:
        print("Logging Out...")
        return db.logOut(msg['sender_id'])
    elif msg_request_type == config.END_SESSION:
        print("Ending session...")
        #TODO: Remove socket from list of sockets
        return ""
    elif msg_request_type == config.ERROR:
        print("Error...")
        return 404
    
def server():
    #Helpful https://realpython.com/python-sockets/
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((config.SERVER_HOST, config.PORT))
        print("Server up on IP: ", config.SERVER_HOST, " and port: ", config.PORT )

        #Create DB Object
        db = DB('test.db')
        print("Server loaded DB: ")

        s.listen()
        print("Server listening...")
        clientsocket, client_addr = s.accept()
        with clientsocket:
            print('Connected by', client_addr)
            while True:
                bdata, addr = clientsocket.recvfrom(1024)
                print("Data from Client Socket: ", clientsocket)
                print("BDATA: ", bdata)
                msg = wire_protocol.unmarshal(bdata)
                print("Got MSSG: ", msg, " from Address: ", client_addr)

                handled_response = handleRequest(msg, db)
                
                response = wire_protocol.marshal(msg['request_type'], 1, -1, handled_response)
                sent = clientsocket.send(response)
                print('Server responded, %d/%d bytes transmitted' % (sent, len(response)))


server()

