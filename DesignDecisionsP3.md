#Paxos

1. We decided to implement a paxos system where each client sends all responses to the server
2. We want to implement a sort of Paxos logic to decide which server's response to use.

#TODO:

1. Paxos logic
2. Exec logic
3. Servers catching up to each other
4.

#If a server goes down that was initially up when a client was started, the client takes a while to send new requets because it waits for a request to time out (10s maybe?)
