import pytest
import config
import wire_protocol

class TestClient:

    def test_client_main(self, mocker):
        x = 1
        assert x == 1