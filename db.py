import datetime
import sqlite3
import string

class DB:
    def __init__(self, db_name='test.db'):
        #Will load the DB in if it exists, or create a new one with the given name if it does not exist
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
    
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

    #Insert and Delete users from account table
    def insertNewUser(self, username: string):

        # Check if the user already exists
        self.cur.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        user = self.cur.fetchone()
        if user:
            print("User already exists.")
            return
        
        # Insert the new user
        self.current_time = datetime.datetime.now()
        self.cur.execute("INSERT INTO accounts (username, logged_in, created_at) VALUES (?, ?, ?)", (username, 0, self.current_time))
        self.con.commit()
        print("User {} added sucsessfully".format(username))
        

    def deleteUser(self, username: string):
        # Check if the user already exists
        self.cur.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        user = self.cur.fetchone()
        if not user:
            print("User {} does not exist.".format(username))
            return
        
        self.cur.execute("DELETE FROM accounts WHERE username=?", (username,))
        self.con.commit()
        print("User {} deleted successfully.".format(username))

    def listAccounts(self, condition: string = "", arguments = []):
        self.cur.execute("SELECT * FROM accounts {}".format(condition), arguments)
        accounts = self.cur.fetchall()
        return accounts

    # def insertMessage(self, sender_username: string, receiver_username: string, content: string, created_at: string):
    #     #Create ID of message
    #     #Check if reciever is loged in

    def printTable(self, table_name: string):
        self.cur.execute("SELECT * FROM {}".format(table_name))
        table = self.cur.fetchall()
        print(table)
    



