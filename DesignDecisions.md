## Server

This will be our source of truth on the accounts available.

### Server Responses

- We had to figure out how to let the client know if a request was succsessful or not. We decided to use the message field of our wire protocal to indicate succsess or failure and any pertinent information. It is passed as a string and then converted to a tuple using the eval function. This means the response data is unstructured. This allows flexibility but also oppertunities for errors parsing.

### Database

- We decided to use a sqlite database that remains persisted. This way whether the server is spun up on one machine or a different machine, the db will remain up to date--so long as the DB is commited to github and only one server is running at a time.
- We created a class that holds all operations associated with the DB. This is because there is both the connection that you want to keep track of and the cursor. The connection is commited each time an update is made to the DB.

- We ran into the problem of how to send messages to users that are logged in. We decied to have a field in the DB that coressponeded to the IP of the signed in User or -1 if they were not logged in.

### Clients connected to server

- While writing our code to enable multiple clients to connect to our server and message back and worth we had to give our server a notion of the clients that were connected. The server than should be able to send messages to these clients and close them out when a user exits their session. We have a dictionary on the server that has a key as the username and the clientsocket as the value. That way, we can keep track of what users are active.

## Client

The client is responsible for interacting with the user and sending messages to the server.

### Authentication

We decided to make authentication easy and simple by not supporting passwords. The user can instead log in via username. Having a user is required to send and receive messages, but we decided not to focus more on authentication for the sake of time and simplicity.

### Sending Messages

The client sends the message to the server with three types of information: receiver, message, and timestamp. The receiver tells the server how to store the message and where to send it. The message is the text to be conveyed. The timestamp allows the server and clients to agree on an order of messages.

### Receiving Messages

There are two flows to consider. The first flow is sending a message to live (logged-in) user. The server maintains a list of IPs for all active users in the DB, so it knows where to send the incoming message to that user client. The second flow is when the client requests all messages received by that user. In this case, the client initiates the request to the server to return all messages for that user.

In both cases, we decided to use the same config request type (RECEIVE_MESSAGES) for simplicity. Ideally we would define two different types for the two flows, but in this case make do with a single request type. It reduces complexity, at the expense of mixing up the right action or response.

## Wire Protocol

We initially used the same wire protocol for both sending and receiving. However this ended up being a problem, as we started to include fields that were specific to just one type. For example, only responses require a response code (success or failure), but we were initialy sending along a dummy response code in the request.

It made more sense to separate requests from responses. Request payloads could then include the fields needed for a request while response payloads could include the fields for a response. This reduces the overall size of the payload and makes each better adapted to its use.

## Questions We Considered

1. Do we want one wire protocol to handle all communication, or separate wire protocols per message type (i.e. account creation vs message sending)?
   A: We need one wire protocol because the server doesn't know what type of reqeust it's receiving. Therefore, the first piece of information to encode in the protocol is the type of request.
2. For the wire protocol, how do we distinguish between the different fields?
   A: We are using the string delimiter "::" for now. Eventually, we would want to escape the user-inputted text to avoid an error if the user enters :: as part of the message.
3. What types of request types do we need to handle in the wire protocol? What types of errors do we need to handle in the wire protocol?
   A: We have defined request types for the main functions: create an account, log in, list users, send a message, etc (defined in the README and config files). For errors, we have decided to keep it simple and return a simple error when an operation is not possible. The client is responsible for interpreting what the error means based on the type of request.
4. What is the limit to the size of the message that a user can send over our protocol? How we do handle messages that require multiple packets to be sent along the wire?
   A: gRPC handles mesages up to length of 10MB. We don't anticipate messages being larger than this. See below for more discussion on message size.
5. How should we refer to users: unique id or username?
   A: If we used unique numbers this would decrease the size of our messages but decided to use usernames as it allows us to keep track of our users more simply.

## GRPC Vs. Original

1. One major difference between our GRPC server and our original one was that in order to get live messages we had to implement polling in gRPC rather than sending live messages as we had done on the original server. To the user the difference is not apparent because we poll the gRPC server every one second for new messages if somebody is logged in. From a network traffic standpoint though, polling every 1 second for new messages is less effecient than having the server simply send new messages to a logged in user whenever they are sent a message by a different user.

   - This affected our logic for sending unsent messages. In our original server we updated if a message was sent or not soley based on if the user was logged in. We then changed on the message in the DB. This doesnt work for the gRPC implementation because we don't immediatly send messages to users even if they are logged in. Thus we have to set it to delivered once we actually deliver the messages in gRPC.

   - TO send unsent messages in the original server we query the DB for any unsent messages when the user logs in and then return any new messages. We then set these messages to having been sent.

2. Size of messages

   - In our original server we used the `recv(num_bytes)` funciton which allowed us to recieve a specificed number of bytes from the server. We used 1024 throughout our client. This meant that if a user had a very long chain of messages with a different user our server would crash because we were sending too many bytes. In gRPC this was not an issue because each message had a maximum size of 4mb which is 4 \* 10^6 bytes. Until this chat program is run at a much larger scale our gRPC server and client will not have an issue with the size of messages.

3. For the gRPC our server had 109 lines while our original server had 159 lines. This 30% reduction was due to the fact that we didnt have add any code to start new threads each time a new client was connected and we didnt have to include logic to recieve each request. With gRPC most of the initialization of the server is done for us with `server.start()`. The gRPC client was 70 lines smaller than the original client. This is because we did not have to add any special logic to parse our respones as gRPC provided messages that were prinatable and readable by the users.
