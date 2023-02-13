## Server

This will be our source of truth on the accounts available.

### Server Responses

- We had to figure out how to let the client know if a request was succsessful or not. We decided to use the message field of our wire protocal to indicate succsess or failure and any pertinent information. It is passed as a string and then converted to a tuple using the eval function. This means the response data is unstructured. This allows flexibility but also oppertunities for errors parsing.

### Database

- We decided to use a sqlite database that remains persisted. This way whether the server is spun up on one machine or a different machine, the db will remain up to date--so long as the DB is commited to github and only one server is running at a time.
- We created a class that holds all operations associated with the DB. This is because there is both the connection that you want to keep track of and the cursor. The connection is commited each time an update is made to the DB.

- We ran into the problem of how to send messages to users that are logged in. We decied to have a field in the DB that coressponeded to the IP of the signed in User or -1 if they were not logged in.

## Client

The client is responsible for interacting with the user and sending messages to the server. 

### Authentication

We decided to make authentication easy and simple by not supporting passwords. The user can instead log in via username. Having a user is required to send and receive messages, but we decided not to focus more on authentication for the sake of time and simplicity.

### Sending Messages

The client sends the message to the server with three types of information: receiver, message, and timestamp. The receiver tells the server how to store the message and where to send it. The message is the text to be conveyed. The timestamp allows the server and clients to agree on an order of messages.

### Receiving Messages

There are two flows to consider. The first flow is sending a message to live (logged-in) user. The server maintains a list of IPs for all active users in the DB, so it knows where to send the incoming message to that user client. The second flow is when the client requests all messages received by that user. In this case, the client initiates the request to the server to return all messages for that user. 

## Questions We Considered

1. Do we want one wire protocol to handle all communication, or separate wire protocols per message type (i.e. account creation vs message sending)?
   A: We need one wire protocol because the server doesn't know what type of reqeust it's receiving. Therefore, the first piece of information to encode in the protocol is the type of request.
2. For the wire protocol, how do we distinguish between the different fields?
   A: We are using the string delimiter "::" for now. Eventually, we would want to escape the user-inputted text to avoid an error if the user enters :: as part of the message.
3. What types of request types do we need to handle in the wire protocol? What types of errors do we need to handle in the wire protocol?
   A: We have defined request types for the main functions: create an account, log in, list users, send a message, etc (defined in the README and config files). For errors, we have decided to keep it simple and return a simple error when an operation is not possible. The client is responsible for interpreting what the error means based on the type of request.
4. What is the limit to the size of the message that a user can send over our protocol? How we do handle messages that require multiple packets to be sent along the wire?
5. How should we refer to users: unique id or username?
   A: If we used unique numbers this would decrease the size of our messages but decided to use usernames as it allows us to keep track of our users more simply.
6. Should we call eval() on message in the wire_protocal or only in instances where we know the response will be a tuple?
