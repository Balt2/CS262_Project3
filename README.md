# CS262_Project1

This is a project to fulfill the requirements of the first design challenges of CS262: Distributed Computing. This README covers to install, setup, run, and test our code. The DesignDecisions doc details our engineering decisions.

## Setup

1. Edit config.py to the IP address of the server host. This will need to be the same value on both the client and server.

   You should use the IP address from the computer itself and not a website like whatismyip, because the IP exposed to the general public is different than the IPv4 from the computer's perspective. On a Mac, for example, the IP can be found by navigating to Settings > Network > Advanced > TCP/IP tab.

2. From the root directory of the repository, run: `pip install grpcio grpcio-tools`.

## Compiling for gRPC

These steps only need to occur after developmental changes. If you just cloned the repo and pulled down the latest you should not need to complete this step. However, if you make any changes to `messages.proto`, you'll need to recompile by performing this step.

1. Navigate to the `grpc` directory and run this command from within that directory: `python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. messages.proto`

This will automatically update the `messages_pb2.py` and `messages_pb2_grpc.py` files for you (or generate them if they don't exist).

## Running Part 1 (The Wire Protocol)

1. On one computer, run client.py. From the root directory of the repository:
   `python client.py`

2. On the other computer, run server.py. From the root directory of the repository:
   `python server.py`

Note: this project assumes the computers are on the same Internet network.

## Running Part 2 (gRPC)

1. On one computer, run client_grpc.py. From the root directory of the repository::
   `python grpc/client_grpc.py`

2. On the other computer, run server_grpc.py. From the root directory of the repository::
   `python grpc/server_grpc.py`

Note: this project assumes the computers are on the same Internet network.

## Testing

We use pytest to run the tests. To run pytest, you'll need both the 'pytest' and 'pytest-mock' libraries.

1. Install the test libraries (one-time only). In the root director of the repository, run: `pip install pytest pytest-mock`
2. Run the tests. In the root directory of the repository, run: `pytest`
