import config

def client_options_menu(logged_in_user=None):
    # print the options menu
    print("\n\n----- Options Menu: please enter the number of your choice from the following options. ----- ")
    menu_str = " 1. Create an account \n 2. Log in \n 3. List Accounts \n"
    if logged_in_user:
        menu_str += " 4. Send a message \n 5. See your messages \n 6. Delete your account \n 7. Log out \n"
    else:
        menu_str += " 4-7: (must log in to see) \n"
    menu_str += " 8. Exit"
    print(menu_str)
    # capture user input, handling errors
    while True:
        try:
            data=(input("Enter a Number: ")) 
            if data.isdigit():
                data = int(data)

                # map user input to request types
                if data == 1:
                    return config.ACCOUNT_CREATION
                if data == 2:
                    return config.LOG_IN
                if data == 3:
                    return config.LIST_ACCOUNTS
                if data == 4:
                    return config.SEND_MESSAGE
                if data == 5:
                    return config.REQUEST_MESSAGES
                if data == 6:
                    return config.ACCOUNT_DELETION
                if data == 7:
                    return config.LOG_OUT
                if data == 8:
                    return config.END_SESSION
            else:
                return config.ERROR
        except ValueError:
            return config.ERROR