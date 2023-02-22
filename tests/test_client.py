import sys
sys.path.append('../CS262_Project1')


import pytest
import wire_protocol
from mock import patch
import client

class MockThread:
    def __init__(self, target):
        self.target = target
    
    def start():
        pass

def mock_input(input_values):
    # mock the user input
    output = []
    def mock_input(s):
        output.append(s)
        return input_values.pop(0)
    client.input = mock_input
    client.print = lambda s : output.append(s)

class TestClient:

    def test_client_log_in(self, mocker):
        with patch.object(client.Client, "__init__", lambda x: None):
            mocker.patch("time.time", return_value = 12345)

            mock_input(["test_username"])

            # the test
            client_mock = client.Client()
            response = client_mock.log_in()
            assert response == b'2::test_username::-1::12345::-1::'

    def test_client_send_message(self, mocker):
        with patch.object(client.Client, "__init__", lambda x: None):
            mocker.patch("time.time", return_value = 12345)

            mock_input(["msg","test_recipient"])

            # the test
            client_mock = client.Client()
            response = client_mock.send_message(sender_id="test_username")
            assert response == b'4::test_username::test_recipient::12345::msg::'

    def test_client_log_out(self, mocker):
        with patch.object(client.Client, "__init__", lambda x: None):
            mocker.patch("time.time", return_value = 12345)

            mock_input(["test_username"])

            # the test
            client_mock = client.Client()
            response = client_mock.log_out()
            assert response == b'7::-1::-1::12345::::'


    def test_client_delete_account(self, mocker):
        with patch.object(client.Client, "__init__", lambda x: None):
            mocker.patch("time.time", return_value = 12345)

            mock_input(["test_username"])

            # the test
            client_mock = client.Client()
            response = client_mock.delete_account()
            assert response == b'6::-1::-1::12345::::'
