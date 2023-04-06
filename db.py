import datetime
import sqlite3
import string
import time
import uuid

class DB:
    def __init__(self, db_name='test.db'):
        #Will load the DB in if it exists, or create a new one with the given name if it does not exist
        self.con = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.con.cursor()
        self.createAccountTable()
        self.createMessageTable()

    
    #Create Tables
    def createAccountTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                            username text PRIMARY KEY,
                                            logged_in integer INTEGER DEFAULT 0 NOT NULL,
                                            created_at text
                                        )''')
        self.con.commit()
    
    def createMessageTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                                            id text PRIMARY KEY,
                                            sender_username text NOT NULL,
                                            reciever_username text NOT NULL,
                                            content text NOT NULL,
                                            delivered integer INTEGER DEFAULT 0 NOT NULL,
                                            created_at text
                                        )''')
        self.con.commit()

    def wipeDBEntries(self):
        self.cur.execute("DELETE FROM accounts")
        self.cur.execute("DELETE FROM messages")
        self.con.commit()
        
    def doesUserExist(self, username: string):
        self.cur.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        user = self.cur.fetchone()
        if user:
            return True
        else:
            return False
        
    #Insert and Delete users from account table
    def insertUser(self, username: string):

        # Check if the user already exists
        if self.doesUserExist(username):
            return 404, "User {} already exists.".format(username)
            
        
        # Insert the new user
        self.current_time = datetime.datetime.now()
        self.cur.execute("INSERT INTO accounts (username, logged_in, created_at) VALUES (?, ?, ?)", (username, 1, self.current_time))
        self.con.commit()
        return 200, username
        

    def deleteUser(self, username: string):
        # Check if the user already exists
        if not self.doesUserExist(username):
            return 404, "User {} does not exist.".format(username)
        
        self.cur.execute("DELETE FROM accounts WHERE username=?", (username,))
        self.con.commit()
        return 200, username

    def logIn(self, username: string):

        # Check if the user already exists
        if not self.doesUserExist(username):
            return 404, "User {} does not exist.".format(username)
        
        # Check if the user is already logged in
        self.cur.execute("SELECT logged_in FROM accounts WHERE username = ?", (username,))
        user = self.cur.fetchone()
        if user[0] == 1:
            return 404, "User {} is already logged in.".format(username)
        
        self.cur.execute("UPDATE accounts SET logged_in = 1 WHERE username = ?", (username,))
        self.con.commit()
        return 200, username
    
    def isUserLoggedIn(self, username: string):
        # Check if the user already exists
        if not self.doesUserExist(username):
            return "User {} does not exist.".format(username)
        
        self.cur.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        user = self.cur.fetchone()
        if user[1] == 1:
            return True
        else:
            return False
        
    def logOut(self, username: string):
        # Check if the user already exists
        if not self.doesUserExist(username):
            return 404, "User {} does not exist.".format(username)
        
        if not self.isUserLoggedIn(username):
            return 404, "User {} is not logged in.".format(username)
        
        self.cur.execute("UPDATE accounts SET logged_in = 0 WHERE username = ?", (username,))
        self.con.commit()
        return 200, username

    def listAccounts(self, condition: string = "", arguments = []):
        self.cur.execute("SELECT * FROM accounts {}".format(condition), arguments)
        accounts = self.cur.fetchall()
        return 200, accounts

    def insertMessage(self, sender_username: string, receiver_username: string, content: string, grpc_server=True):
        #Check if sender exist
        if not self.doesUserExist(sender_username):
            return 404, "Sender {} does not exist.".format(sender_username)
        
        #Check if reciever exists
        if not self.doesUserExist(receiver_username):
            return 404, "Reciever {} does not exist.".format(receiver_username)
        
        #Check if reciever is the same as the sender
        if sender_username == receiver_username:
            return 404, "Sender {} cannot send a message to themselves.".format(sender_username)
        
        delivered = 0
        print("CHECKING IF USER IS LOGGED IN")
        if not grpc_server and self.isUserLoggedIn(receiver_username):
            print("USER IS LOGGED IN!")
            delivered = 1
        else:
            print("USER IS NOT LOGGED IN")

        #Create ID of message
        id = str(uuid.uuid4())
        #Insert message into table
        self.cur.execute("INSERT INTO messages (id, sender_username, reciever_username, content, delivered, created_at) VALUES (?, ?, ?, ?, ?, ?)", (id, sender_username, receiver_username, content, delivered, str(time.time())))
        self.printTable("messages")
        self.con.commit()
        return 200, str(delivered)
    
    def forceInsertListOfMessages(self, messages: list):
        for message in messages:
            self.cur.execute("INSERT INTO messages (id, sender_username, reciever_username, content, delivered, created_at) VALUES (?, ?, ?, ?, ?, ?)", (message.id, message.sender_id, message.receiver_id, message.content, message.delivered, message.created_at))
        
        return 200, "Messages inserted successfully."
    
    def forceInsertListOfAccounts(self, accounts: list):
        for account in accounts:
            self.cur.execute("INSERT INTO accounts (username, logged_in, created_at) VALUES (?, ?, ?)", (account.username, account.logged_in, account.created_at))
        
        return 200, "Accounts inserted successfully."
    
    def getMessagesForChat(self, username: string, receiver_username: string = None):
        #Check if user exists
        if not self.doesUserExist(username):
            return 404, "User {} does not exist.".format(username)
        
        if not self.doesUserExist(receiver_username):
            return 404, "User {} does not exist.".format(receiver_username)
        #Get messages for user
        self.cur.execute('''
        SELECT * FROM messages 
        WHERE (sender_username = ? AND reciever_username = ?) 
        OR (sender_username = ? AND reciever_username = ?)
        ORDER BY created_at DESC
        ''', (username, receiver_username, receiver_username, username))
        messages = self.cur.fetchall()
        return 200, messages
    
    def getUndeliveredMessagesForUser(self, username: string):
        #Check if user exists
        if not self.doesUserExist(username):
            return 404, "User {} does not exist.".format(username)
        
        self.printTable("messages")
        #Get messages for user
        self.cur.execute('''
        SELECT * FROM messages 
        WHERE reciever_username = ? 
        AND delivered = 0 
        ORDER BY created_at DESC
        ''', (username,))
        messages = self.cur.fetchall()


        if len(messages) == 0:
            return 201, "No new messages"
        #Set messages to delivered
        self.cur.execute('''
        UPDATE messages SET delivered = 1  
        WHERE reciever_username = ? 
        AND delivered = 0 
        ''', (username,))

        #Return messages
        return 200, messages
    
    def listMessages(self, condition: string = "", arguments = []):
        try:
            self.cur.execute("SELECT * FROM messages {}".format(condition), arguments)
            messages = self.cur.fetchall()
            return 200, messages
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            return 404, e.args[0]


    
    def deleteMessagesForUser(self, username: string):
        #Check if user exists
        if not self.doesUserExist(username):
            return 404
        
        self.cur.execute("DELETE FROM messages WHERE reciever_username = ?", (username,))
        self.cur.execute("DELETE FROM messages WHERE sender_username = ?", (username,))
        self.con.commit()
        return 200, "Messages for and to user {} deleted successfully.".format(username)


    def printTable(self, table_name: string):
        self.cur.execute("SELECT * FROM {}".format(table_name))
        table = self.cur.fetchall()
        print(table)
    



