import sys
sys.path.append('../CS262_Project1')

import server_utils

class TestServerUtils:

    def test_include_account_wildcard(self, mocker):
       assert True == server_utils.should_include_account('username', '*')

    def test_not_include_account(self, mocker):
       assert False == server_utils.should_include_account('username', 'b')

    def test_include_account_single_letter(self, mocker):
       assert True == server_utils.should_include_account('username', 'u')

    def test_include_account_single_letter_wildcard(self, mocker):
       assert True == server_utils.should_include_account('username', 'u*')

    def test_include_account_exact(self, mocker):
       assert True == server_utils.should_include_account('username', 'username')       