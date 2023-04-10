## Server

For this project, we decided to hard code in 3 servers. This allows to demonstrate fault tolerance without having to worry about an infinitely scalable system. If we were to build an infinitely scalable system, we would have to make some different decisions.

### Server State

The clients communicate with all of the servers. This allows each server to continue to maintain the proper state. If a server goes down and comes back, it polls the other servers and asks them for their logical clock. The clock is a simple count of the number of client-side requests that have come in. If another server has a logical clock that is greater than its own, the polling server asks that server for its current state in order to be up-to-date. The clock is a good proxy for being able to tell if a server is behind.

We decided to not use a time-clock because a newly-spawned server could serve a request immediately upon start, at which point it's clock for most-recent transaction would be considered up-to-date. It would have missed out on all of the transactions that happened while it was offline, however. The use of a logical clock allows to sequence transactions and figure out if a server is behind the others.

### Server Database

Each server maintains its own local DB. The DB state gets shared between servers whenever one goes down and comes back online. In a true distributed system, we would have maintained a log of operations, such that we could send those operations to the new system to catch it up. In our case, however, we found it simpler just to send the entire state over to the server. This works for this project but would not work if the database itself was much larger.

### Server Architecture

We decided to have the clients connect to every server, rather than use a primary-backup architecture. Because we're working with a defined system of 3 servers, this is feasible; in an infinitely scalable system this would not work. However, for simplicity, the clients know about and connect with each server. This allows the servers to stay up-to-date with ongoing transactions. The server-to-server communication only needs to happen when a server goes down and comes back up. This minimizes the number of times that the servers must share state with each other.

## Client

### Consensus

The client asks each server for the correct response. If there is a majority response (i.e. 2 or more servers agree on the same response), then that is selected as the reponse and shown to the user. If there is no agreement, the client selects the first response and shows that to the user.

### Server Connections

The client maintains a list of active and inactive server connections. It periodically attempts to reconnect to inactive server connections, so that it can reconnect to a server that goes down and comes back up. This works because, again, each client knows about the 3 servers. If we could not hard-code this part in, we would have to use a different approach.
