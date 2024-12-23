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
    def list_users(cls, headers={}):
        return NetworkRequest.get(cls._get_url('/users'), headers=headers)

    @classmethod
    def create_user(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/users'), data, headers=headers)

    @classmethod
    def get_user(cls, user_id, headers={}):
        return NetworkRequest.get(cls._get_url(f'/users/{user_id}'), headers=headers)

    @classmethod
    def login(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/auth'), data, headers=headers)

    @classmethod
    def token_gen(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/auth/token'), data, headers=headers)

    @classmethod
    def list_tweets(cls, headers={}):
        return NetworkRequest.get(cls._get_url('/tweets'), headers=headers)

    @classmethod
    def create_tweet(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/tweets'), data, headers=headers)

    @classmethod
    def get_tweet(cls, tweet_id, headers={}):
        return NetworkRequest.get(cls._get_url(f'/tweets/{tweet_id}'), headers=headers)

    @classmethod
    def update_tweet(cls, tweet_id, data, headers={}):
        return NetworkRequest.put(cls._get_url(f'/tweets/{tweet_id}'), data, headers=headers)

    @classmethod
    def delete_tweet(cls, tweet_id, headers={}):
        return NetworkRequest.delete(cls._get_url(f'/tweets/{tweet_id}'), headers=headers)

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
    def __str__(self):
        return f'Access Token: {self.access_token}, Refresh Token: {self.refresh_token}'


def retry_mechanism(func):
    def inner(self,*args, **kwargs):
        returnValue = func(self,*args, **kwargs)
        if returnValue['code'] == 401:
            self.auth.change_access_token()
            return func(self,*args, **kwargs)
        return returnValue
    return inner

class Twitter:
    def __init__(self, username=None, password=None):
        self.auth = Auth(username, password)

    @retry_mechanism
    def list_tweets(self):
        return TwitterRequestHandler.list_tweets(headers={'Authorization': f'Bearer {self.auth.access_token}'})

    @retry_mechanism
    def create_tweet(self, data):
        return TwitterRequestHandler.create_tweet(data, headers={'Authorization': f'Bearer {self.auth.access_token}'})

    @retry_mechanism
    def get_tweet(self, tweet_id):
        return TwitterRequestHandler.get_tweet(tweet_id, headers={'Authorization': f'Bearer {self.auth.access_token}'})

    @retry_mechanism
    def update_tweet(self, tweet_id, data):
        return TwitterRequestHandler.update_tweet(tweet_id, data, headers={'Authorization': f'Bearer {self.auth.access_token}'})

    @retry_mechanism
    def delete_tweet(self, tweet_id):
        return TwitterRequestHandler.delete_tweet(tweet_id, headers={'Authorization': f'Bearer {self.auth.access_token}'})    



print(TwitterRequestHandler.list_users())

twitter = Twitter('adib', '1234')

print(twitter.auth)
