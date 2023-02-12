## Server

This will be our source of truth on the accounts available.

### Database

- We decided to use a sqlite database that remains persisted. This way whether the server is spun up on one machine or a different machine, the db will remain up to date--so long as the DB is commited to github and only one server is running at a time.
- We created a class that holds all operations associated with the DB. This is because there is both the connection that you want to keep track of and the cursor. The connection is commited each time an update is made to the DB.

## Client

### Messages

Client messages will be stored with the client and queue until a server is availble. Once a server becomes available the queue will send all messages to the server

## Questions We Considered

1. Do we want one wire protocol to handle all communication, or separate wire protocols per message type (i.e. account creation vs message sending)?
   A: We need one wire protocol because the server doesn't know what type of reqeust it's receiving. Therefore, the first piece of information to encode in the protocol is the type of request.
2. For the wire protocol, how do we distinguish between the different fields?
   A: We are using the string delimiter "::" for now. Eventually, we'll need to escape the user-inputted text to avoid an error if the user enters :: as part of the message.
3. What types of request types do we need to handle in the wire protocol? What types of errors do we need to handle in the wire protocol?
4. What is the limit to the size of the message that a user can send over our protocol? How we do handle messages that require multiple packets to be sent along the wire?
