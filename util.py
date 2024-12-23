import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError


class NetworkRequest:
    @staticmethod
    def _create_request(url, method, data=None, headers={}):
        if data:
            data = json.dumps(data).encode('utf-8')
        req = Request(url=url, method=method,data=data, headers=headers)
        if data:
            req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        
        
        result = {}
        try:
            with urlopen(req) as res:
                body = res.read().decode('utf-8')
                result['body'] = json.loads(body)
                result['code'] = res.status
        except HTTPError as e:
            result['body'] = json.loads(e.read().decode('utf-8'))
            result['code'] = e.code
        except Exception as e:
            result['body'] = str(e)
            result['code'] = 500
        return result
        
    @staticmethod
    def get(url, headers = {}):
        return NetworkRequest._create_request(url,'GET',headers=headers)    
    @staticmethod
    def post(url, data, headers = {}):
        return NetworkRequest._create_request(url,'POST',data,headers)
    @staticmethod
    def put(url, data, headers = {}):
        return NetworkRequest._create_request(url,'PUT',data,headers)
    @staticmethod
    def delete(url, headers = {}):
        return NetworkRequest._create_request(url,'DELETE',headers=headers)
        

class TwitterRequestHandler:
    base_url = 'http://localhost:8000/api'

    @classmethod
    def _get_url(cls, endpoint):
        return f"{cls.base_url}{endpoint}"

    @classmethod
    def list_users(cls):
        return NetworkRequest.get(cls._get_url('/users'))

    @classmethod
    def create_user(cls, data):
        return NetworkRequest.post(cls._get_url('/users'), data)

    @classmethod
    def get_user(cls, user_id):
        return NetworkRequest.get(cls._get_url(f'/users/{user_id}'))

    @classmethod
    def login(cls, data):
        return NetworkRequest.post(cls._get_url('/auth'), data)

    @classmethod
    def token_gen(cls, data):
        return NetworkRequest.post(cls._get_url('/auth/token'), data)

    @classmethod
    def list_tweets(cls):
        return NetworkRequest.get(cls._get_url('/tweets'))

    @classmethod
    def create_tweet(cls, data):
        return NetworkRequest.post(cls._get_url('/tweets'), data)

    @classmethod
    def get_tweet(cls, tweet_id):
        return NetworkRequest.get(cls._get_url(f'/tweets/{tweet_id}'))

    @classmethod
    def update_tweet(cls, tweet_id, data):
        return NetworkRequest.put(cls._get_url(f'/tweets/{tweet_id}'), data)

    @classmethod
    def delete_tweet(cls, tweet_id):
        return NetworkRequest.delete(cls._get_url(f'/tweets/{tweet_id}'))

class Auth:
    def __init__(self, username=None, password=None):
        self.login(username, password)

    def login(self, username, password):
        try:
            body = TwitterRequestHandler.login({'username': username, 'password': password})['body']
            self.refresh_token = body['refresh_token']
            self.access_token = body['access_token']
        except:
            self.refresh_token = None
            self.access_token = None
            print('Error: Could not login')
    def change_access_token(self):
        try:
            body = TwitterRequestHandler.token_gen({'refresh_token': self.refresh_token})['body']
            self.access_token = body['access_token']
            self.refresh_token = body['refresh_token']
        except:
            self.access_token = None
            print('Error: Could not generate access token')

    
