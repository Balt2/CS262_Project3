import datetime
import socket
import string
import config
import sqlite3

from db import DB


def connectToDB() -> sqlite3.Cursor:
    #Connect to test.db if exists, otherwise create it
    con = sqlite3.connect('test.db')
    #Get cursor for dabatase
    cur = con.cursor()
    return cur

def createAccountTable(cur: sqlite3.Cursor):
    cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                        username text PRIMARY KEY,
                                        logged_in integer INTEGER DEFAULT 0 NOT NULL,
                                        created_at text
                                    )''')
    
def createMessageTable(cur: sqlite3.Cursor):
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                                        id text PRIMARY KEY,
                                        sender_username text NOT NULL,
                                        reciever_username text NOT NULL,
                                        content text NOT NULL,
                                        delivered integer INTEGER DEFAULT 0 NOT NULL,
                                        created_at text
                                    )''')

def insertNewUser(cur: sqlite3.Cursor, username: string):

    # Check if the user already exists
    cur.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    user = cur.fetchone()
    if user:
        print("User already exists.")
        return
    
     # Insert the new user
    current_time = datetime.datetime.now()
    cur.execute("INSERT INTO accounts (username, logged_in, created_at) VALUES (?, ?, ?)", (username, 0, current_time))

def deleteUser(cur: sqlite3.Cursor, username: string):
    # Check if the user already exists
    cur.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    user = cur.fetchone()
    if not user:
        print(f"User {username} does not exist.")
        return
    
    cur.execute("DELETE FROM accounts WHERE username=?", (username,))
    print(f"User {username} deleted successfully.")
    


def listAccounts(cur: sqlite3.Cursor, condition: string = "", arguments = []):
    cur.execute("SELECT * FROM accounts {}".format(condition), arguments)
    accounts = cur.fetchall()
    return accounts

def printTable(cur: sqlite3.Cursor, table_name: string):
    cur.execute("SELECT * FROM {}".format(table_name))
    table = cur.fetchall()
    print(table)

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

# con = sqlite3.connect('test.db')
# cur = con.cursor()
# createAccountTable(cur)
# createMessageTable(cur)
# insertNewUser(cur, "dlim1")
# printTable(cur, "accounts")
# print(listAccounts(cur, "WHERE username = ?", ["balt2"]))
# con.commit()

server()

