## Server
This will be our source of truth on the accounts available.

## Client
### Messages
Client messages will be stored with the client and queue until a server is availble. Once a server becomes available the queue will send all messages to the server




## Questions We Considered
1. Do we want one wire protocol to handle all communication, or separate wire protocols per message type (i.e. account creation vs message sending)?
    A: We need one wire protocol because the server doesn't know what type of reqeust it's receiving. Therefore, the first piece of information to encode in the protocol is the type of request.
2. For the wire protocol, how do we distinguish between the different fields?
3. What types of request types do we need to handle in the wire protocol? What types of errors do we need to handle in the wire protocol?