import sys
sys.path.append('../CS262_Project1')

import client_utils

class TestClientUtils:

    def test_client_options_menu_logged_out(self, mocker):
        input_values = ["1"]
        output = []
    
        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        client_utils.input = mock_input
        client_utils.print = lambda s : output.append(s)
    
        client_utils.client_options_menu(None)
    
        assert output == [
            '\n'
            '\n'
            '----- Options Menu: please enter the number of your choice from the following options. ----- ',
            ' 1. Create an account \n 2. Log in \n 3. List Accounts \n' 
            ' 4-7: (must log in to see) \n'
            ' 8. Exit',
            'Enter a Number: '
        ]

