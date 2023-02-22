import datetime
import re


def should_include_account(username, search_pattern):
    if search_pattern == "*":
        return True
    elif "*" in search_pattern:
        index = search_pattern.index('*')
        if username[0:index] == search_pattern[0:index]:
            return True
    else:
        if re.match(search_pattern, username):
            return True

    return False

def timestamp_to_string(timestamp):
    intTimestamp = int((timestamp).split(".", 1)[0])
    timestamp = datetime.datetime.fromtimestamp(intTimestamp).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp