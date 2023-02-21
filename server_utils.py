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
    