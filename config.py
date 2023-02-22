SERVER_HOST = 'localhost'
PORT = 6000
GRPC_PORT = 6010

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
