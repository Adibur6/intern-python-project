import pytest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError
import json
from util import NetworkRequest

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.status = 200
    mock.read.return_value = json.dumps({"key": "value"}).encode('utf-8')
    return mock

@pytest.fixture
def mock_error_response():
    mock = MagicMock()
    mock.code = 404
    return mock

@pytest.fixture
def mock_error():
    return HTTPError(
        url='http://test.com',
        code=404,
        msg='Not Found',
        hdrs={},
        fp=None
    )

class TestNetworkRequest:
    @patch('util.urlopen')
    def test_get_request(self, mock_urlopen, mock_response):
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = NetworkRequest.get('http://test.com')
        
        assert result['code'] == 200
        assert result['body'] == {"key": "value"}
        
    @patch('util.urlopen')
    def test_post_request(self, mock_urlopen, mock_response):
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        data = {"test": "data"}
        result = NetworkRequest.post('http://test.com', data)
        
        assert result['code'] == 200
        assert result['body'] == {"key": "value"}
        
    @patch('util.urlopen')  
    def test_headers(self, mock_urlopen, mock_response):
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        headers = {'Authorization': 'Bearer token'}
        NetworkRequest.get('http://test.com', headers)
        
        args, _ = mock_urlopen.call_args
        request = args[0]
        assert request.headers['Authorization'] == 'Bearer token'
        assert request.headers['Accept'] == 'application/json'

    @patch('util.urlopen')
    def test_network_request_error(self,mock_urlopen, mock_error):
        mock_urlopen.side_effect = mock_error
        
        result = NetworkRequest.get('http://test.com')
        
        assert result['code'] == 404
        assert 'Not Found' in result['body']