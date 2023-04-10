# CS262_Project3

This is a project to fulfill the requirements of the third design challenges of CS262: Distributed Computing. This README covers to install, setup, run, and test our code. The DesignDecisions doc details our engineering decisions.

## Setup

1. Edit config.py to the IP address of the server hosts. This will need to be the same value on both the client and server.

   You should use the IP address from the computer itself and not a website like whatismyip, because the IP exposed to the general public is different than the IPv4 from the computer's perspective. On a Mac, for example, the IP can be found by navigating to Settings > Network > Advanced > TCP/IP tab.

2. From the root directory of the repository, run: `pip install grpcio grpcio-tools`.

## Compiling for gRPC

These steps only need to occur after developmental changes. If you just cloned the repo and pulled down the latest you should not need to complete this step. However, if you make any changes to `messages.proto`, you'll need to recompile by performing this step. Same for `server_message.proto`. (If you only change one file, you only need to run the appropriate command for that file.)

1. Run this command from the root directory: `python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. messages.proto`

This will automatically update the `messages_pb2.py` and `messages_pb2_grpc.py` files for you (or generate them if they don't exist).

2. Run this command from the root directory: `python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. server_messages.proto`

This will automatically update the `server_messages_pb2.py` and `server_messages_pb2_grpc.py` files for you (or generate them if they don't exist).

## Running

1. On one computer, run client_grpc.py. From the root directory of the repository: `python client_grpc.py`.

2. One that same computer, open two new terminal windows. In each window, from the root directory of the repository: `python server_grpc.py`. You will be asked for the server number. Input 0 for one and 1 for the other.

2. On the other computer, run both the client and server (again). From the root directory of the repository:
   `python server_grpc.py`, then etner server #2 when asked. In another window: `python client_grpc.py`.

Note: this project assumes the computers are on the same Internet network.

## Testing

We use pytest to run the tests. To run pytest, you'll need both the 'pytest' and 'pytest-mock' libraries.

1. Install the test libraries (one-time only). In the root director of the repository, run: `pip install pytest pytest-mock`
2. Run the tests. In the root directory of the repository, run: `pytest`
