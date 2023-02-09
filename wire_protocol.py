import time
import config

def marshal(request_type, sender_id, receiver_id=None, message=''):
    # create a msg object of the values
    msg = {
        'request_type': request_type,
        'sender_id': sender_id,
        'receiver_id': -1,
        'timestamp': time.time(),
        'message': message
    }

    if receiver_id is not None:
        msg["receiver_id"] = receiver_id
        
    # convert the msg object into a single string, with :: as the delimiter between fields
    marshaled_str = ""
    for key in msg:
        marshaled_str += str(msg[key]) + "::"

    # return the marshaled string, encoded into ascii
    return marshaled_str.encode('ascii')

def unmarshal(bdata):
    str = bdata.decode('ascii')
    split_str = str.split("::") 

    if len(split_str) != 6:
        raise Exception('Unable to unmarshal the message')

    msg = {}
    for i, item in enumerate(split_str):
        if i == 0:
            msg['request_type'] = int(item)
        if i == 1:
            msg['sender_id'] = int(item)
        if i == 2:
            msg['receiver_id'] = int(item)
        if i == 3:
            msg['timestamp'] = float(item)
        if i == 4:
            msg['message'] = item

    return msg