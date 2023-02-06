import socket
import config
import wire_protocol

# dummy file to help test client functions, will delete after development

print("main")
msg = wire_protocol.marshal(config.LIST_ACCOUNTS, 23, 4, "test marshal message")
print(msg)
unmarshall = wire_protocol.unmarshal(msg)
print(unmarshall)
print("close")