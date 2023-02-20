import time
import config

def marshal_into_single_string(msg):
    # convert the msg object into a single string, with :: as the delimiter between fields
    marshaled_str = ""
    for key in msg:
        marshaled_str += str(msg[key]) + "::"
    return marshaled_str


def marshal_request(request_type, sender_id = '-1', receiver_id = '-1', message=''):
    # create a msg object of the values
    msg = {
        'request_type': request_type,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'timestamp': time.time(),
        'message': message
    }
        
    # return the marshaled string, encoded into ascii 
    marshaled_str = marshal_into_single_string(msg)
    return marshaled_str.encode('ascii')

def unmarshal_request(bdata):
    str = bdata.decode('ascii')
    split_str = str.split("::") 

    if len(split_str) != 6:
        print("ERROR STR: ", str)
        raise Exception('Unable to unmarshal the request')

    msg = {}
    for i, item in enumerate(split_str):
        if i == 0:
            msg['request_type'] = int(item)
        if i == 1:
            msg['sender_id'] = item
        if i == 2:
            msg['receiver_id'] = item
        if i == 3:
            msg['timestamp'] = float(item)
        if i == 4:
            msg['message'] = item

    return msg


def marshal_response(request_type, response_code = 0, message=''):
    # create a msg object of the values
    msg = {
        'response_code': response_code,
        'response_type': request_type,
        'timestamp': time.time(),
        'message': message
    }
        
    # return the marshaled string, encoded into ascii 
    marshaled_str = marshal_into_single_string(msg)
    return marshaled_str.encode('ascii')

def unmarshal_response(bdata):
    str = bdata.decode('ascii')
    split_str = str.split("::") 

    if len(split_str) != 5:
        print("ERROR STR: ", str)
        raise Exception('Unable to unmarshal the response')

    msg = {}
    for i, item in enumerate(split_str):
        if i == 0:
            msg['response_code'] = int(item)
        if i == 1:
            msg['response_type'] = int(item)
        if i == 2:
            msg['timestamp'] = float(item)
        if i == 3:
            msg['message'] = item
        
    return msg