# CS262_Project1

## Setup

1. Edit config.py to the IP address of the server host.

2. On one computer, run client.py.
`python client.py`

3. On the other computer, run server.py.
`python server.py`

Note: this project assumes the computers are on the same Internet network

## Testing

We use pytest to run the tests. To run pytest, you'll need both the 'pytest' and 'pytest-mock' libraries.

1. Install the test libraries (one-time only). In the root director of the repository, run: `pip install pytest pytest-mock`
2. Run the tests. From the command line, in the root directory of the repository, run: `pytest`

## Tasks to Complete

[] Account creation, listing, deletion
[] Send message from one account to another account
    [] database of messages on the server
[] Deliver message to account
[] View messages by account


## Wire Protocol
* Request Type (enum) 
* Sender ID 
* Receiver ID (if needed, -1 otherwise)
* Timestamp
* Message (if needed, '' otherwise)






