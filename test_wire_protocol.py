import pytest
import config
import wire_protocol

class TestWireProtocol:

    def test_marshal_request(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal_request(config.SEND_MESSAGE, 'jim', 4, "test marshal message")
        output_str = output.decode('ascii')
        assert output_str == '4::jim::4::12345::test marshal message::'

    def test_marshal_request_no_sender(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal_request(config.ACCOUNT_CREATION)
        output_str = output.decode('ascii')
        assert output_str == "1::-1::-1::12345::::"

    def test_marshal_request_no_receiver(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal_request(config.LIST_ACCOUNTS, 9)
        output_str = output.decode('ascii')
        assert output_str == "3::9::-1::12345::::"

    def test_unmarshal_request(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        msg = '3::jim::waldo::12345::test unmarshal message::'.encode('ascii')
        output = wire_protocol.unmarshal_request(msg)

        msg = {
            'request_type': 3,
            'sender_id': 'jim',
            'receiver_id': 'waldo',
            'timestamp': 12345,
            'message': "test unmarshal message"
        }
        
        assert output == msg

    def test_unmarshal_request_exception_blank(self):
        with pytest.raises(Exception) as exception_info:
            wire_protocol.unmarshal_request('')
    
    def test_unmarshal_request_exception_short_string(self):
        with pytest.raises(Exception) as exception_info:
            test_str = '3::jim::4::12345::'.encode('ascii')
            wire_protocol.unmarshal_request(test_str)
    
    def test_unmarshal_request_exception_not_binary(self):
        with pytest.raises(Exception) as exception_info:
            wire_protocol.unmarshal_request('this is not binary data')

    def test_marshal_response_success(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal_response(200, "some username")
        output_str = output.decode('ascii')
        assert output_str == '200::12345::some username::'

    def test_marshal_response_error(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal_response(404, "")
        output_str = output.decode('ascii')
        assert output_str == '404::12345::::'

    def test_unmarshal_response(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        msg = '200::12345::test unmarshal response::'.encode('ascii')
        output = wire_protocol.unmarshal_response(msg)

        msg = {
            'response_code': 200,
            'timestamp': 12345,
            'message': "test unmarshal response"
        }
        
        assert output == msg