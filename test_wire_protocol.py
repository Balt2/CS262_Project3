import pytest
import config
import wire_protocol

class TestWireProtocol:

    def test_marshal(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal(config.SEND_MESSAGE, 'jim', 4, "test marshal message")
        output_str = output.decode('ascii')
        assert output_str == '4::jim::4::12345::test marshal message::'

    def test_marshal_no_sender(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal(config.ACCOUNT_CREATION)
        output_str = output.decode('ascii')
        assert output_str == "1::-1::-1::12345::::"

    def test_marshal_no_receiver(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        output = wire_protocol.marshal(config.LIST_ACCOUNTS, 9)
        output_str = output.decode('ascii')
        assert output_str == "3::9::-1::12345::::"

    def test_unmarshal(self, mocker):
        mocker.patch("time.time", return_value = 12345)
        msg = '3::jim::waldo::12345::test unmarshal message::'.encode('ascii')
        output = wire_protocol.unmarshal(msg)

        msg = {
            'request_type': 3,
            'sender_id': 'jim',
            'receiver_id': 'waldo',
            'timestamp': 12345,
            'message': "test unmarshal message"
        }
        
        assert output == msg

    def test_unmarshal_exception_blank(self):
        with pytest.raises(Exception) as exception_info:
            wire_protocol.unmarshal('')
    
    def test_unmarshal_exception_short_string(self):
        with pytest.raises(Exception) as exception_info:
            test_str = '3::jim::4::12345::'.encode('ascii')
            wire_protocol.unmarshal(test_str)
    
    def test_unmarshal_exception_not_binary(self):
        with pytest.raises(Exception) as exception_info:
            wire_protocol.unmarshal('this is not binary data')