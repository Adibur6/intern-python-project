import pytest
from unittest.mock import patch, MagicMock
from util import TwitterRequestHandler

@pytest.fixture
@patch('util.NetworkRequest')
def mock_network(mocke):
    mocke.get.return_value = {'code': 200, 'body': 'success'}
    mocke.post.return_value = {'code': 200, 'body': 'success'}
    mocke.delete.return_value = {'code': 200, 'body': 'success'}
    return mocke

@pytest.fixture
def mock_network():
    with patch('util.NetworkRequest') as mock:
        mock.get.return_value = {'code': 200, 'body': 'success'}
        mock.post.return_value = {'code': 200, 'body': 'success'}
        mock.delete.return_value = {'code': 200, 'body': 'success'}
        yield mock

class TestTwitterRequestHandlerLogging:
    
    @patch('time.perf_counter', side_effect=[1.0, 2.0])
    def test_list_tweets_logging(self, mock_time, mock_network, capsys):
        TwitterRequestHandler.list_tweets()
        
        captured = capsys.readouterr()
        assert "Function list_tweets took 1.0 seconds" in captured.out
        assert mock_time.call_count == 2
        assert mock_network.get.called

    @patch('time.perf_counter', side_effect=[1.0, 2.0])
    def tes_create_tweet_logging(self, mock_time, mock_network, capsys):
        TwitterRequestHandler.create_tweet({"content": "test"})
        
        captured = capsys.readouterr()
        assert "Function create_tweet took 1.0 seconds" in captured.out
        assert mock_time.call_count == 2
        assert mock_network.post.called

    @patch('time.perf_counter', side_effect=[1.0, 2.0])
    def tes_delete_tweet_logging(self, mock_time, mock_network, capsys):
        TwitterRequestHandler.delete_tweet("123")
        
        captured = capsys.readouterr()
        assert "Function delete_tweet took 1.0 seconds" in captured.out
        assert mock_time.call_count == 2
        assert mock_network.delete.called