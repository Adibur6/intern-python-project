from unittest.mock import patch, Mock
import pytest
from util import Twitter

@pytest.fixture
def mock_auth():
    auth = Mock()
    auth.access_token = "initial_token"
    return auth

@pytest.fixture
@patch('util.Auth')
def twitter(MockAuth,mock_auth):
    MockAuth.return_value = mock_auth
    return Twitter("test_user", "test_pass")

class TestTwitterRetry:
    @patch('util.TwitterRequestHandler')
    def test_retry_on_401(self, mock_handler, twitter, mock_auth):
        # First call returns 401, second call succeeds
        mock_handler.list_tweets.side_effect = [
            {'code': 401, 'body': 'Unauthorized'},
            {'code': 200, 'body': 'Success'}
        ]
        
        result = twitter.list_tweets()
        
        assert mock_auth.change_access_token.called
        assert mock_handler.list_tweets.call_count == 2
        assert result['code'] == 200

    @patch('util.TwitterRequestHandler')
    def test_no_retry_on_success(self, mock_handler, twitter, mock_auth):
        mock_handler.list_tweets.return_value = {
            'code': 200, 
            'body': 'Success'
        }
        
        result = twitter.list_tweets()
        
        assert not mock_auth.change_access_token.called
        assert mock_handler.list_tweets.call_count == 1
        assert result['code'] == 200

    @patch('util.TwitterRequestHandler')
    def test_no_retry_on_non_401_error(self, mock_handler, twitter, mock_auth):
        mock_handler.list_tweets.return_value = {
            'code': 404, 
            'body': 'Not Found'
        }
        
        result = twitter.list_tweets()
        
        assert not mock_auth.change_access_token.called
        assert mock_handler.list_tweets.call_count == 1
        assert result['code'] == 404