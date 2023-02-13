# CS262_Project1

This is a project to fulfill the requirements of the first design challenges of CS262: Distributed Computing.

## Setup

1. Edit config.py to the IP address of the server host. This will need to be the same value on both the client and server.

   You should use the IP address from the computer itself and not a website like whatismyip, because the IP exposed to the general public is different than the IPv4 from the computer's perspective. On a Mac, for example, the IP can be found by navigating to Settings > Network > Advanced > TCP/IP tab.

2. On one computer, run client.py. From the root directory of the repository:
   `python client.py`

3. On the other computer, run server.py. From the root directory of the repository:
   `python server.py`

Note: this project assumes the computers are on the same Internet network

## Testing

We use pytest to run the tests. To run pytest, you'll need both the 'pytest' and 'pytest-mock' libraries.

1. Install the test libraries (one-time only). In the root director of the repository, run: `pip install pytest pytest-mock`
2. Run the tests. From the command line, in the root directory of the repository, run: `pytest`

## Wire Protocol

- Request Type (enum)
- Sender ID (if needed, -1 otherwise)
- Receiver ID (if needed, -1 otherwise)
- Timestamp
- Message (if needed, '' otherwise)
