SERVER_HOSTS = [
    ['10.250.25.239', 6010, 6011 ], 
    ['10.250.25.239', 6012, 6013 ],
    ['10.250.78.113', 6014, 6015 ]
]


## Wire Protocol Definitions

# Request Types, used to identify the type of request in the eye of the client
ACCOUNT_CREATION = 1
LOG_IN = 2
LIST_ACCOUNTS = 3
SEND_MESSAGE = 4
REQUEST_MESSAGES = 5
ACCOUNT_DELETION = 6
LOG_OUT = 7
END_SESSION = 8
RECEIVE_MESSAGE = 9
ERROR = 10
NEW_MESSAGES = 11
