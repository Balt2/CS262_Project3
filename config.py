SERVER_HOSTS = [
    ['10.228.146.16', 6010 ], 
    ['10.228.146.16', 6011 ],
    ['10.228.146.13', 6012 ]
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
