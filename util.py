import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def logging_time(func):
    def inner(*args, **kwargs):
        import time
        start = time.time()
        returnValue = func(*args, **kwargs)
        end = time.time()
        print(f'Function {func.__name__} took {end-start} seconds')
        return returnValue
    return inner
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
        except Exception as e:
            result['body'] = str(e)
            result['code'] = e.code
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
    @logging_time
    def list_users(cls, headers={}):
        return NetworkRequest.get(cls._get_url('/users'), headers=headers)

    @classmethod
    @logging_time
    def create_user(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/users'), data, headers=headers)

    @classmethod
    @logging_time
    def get_user(cls, user_id, headers={}):
        return NetworkRequest.get(cls._get_url(f'/users/{user_id}'), headers=headers)

    @classmethod
    @logging_time
    def login(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/auth'), data, headers=headers)

    @classmethod
    @logging_time
    def token_gen(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/auth/token'), data, headers=headers)

    @classmethod
    @logging_time
    def list_tweets(cls,skip=0,limit=1000000, headers={}):
        return NetworkRequest.get(cls._get_url(f'/tweets?skip={skip}&limit={limit}'), headers=headers)

    @classmethod
    @logging_time
    def create_tweet(cls, data, headers={}):
        return NetworkRequest.post(cls._get_url('/tweets'), data, headers=headers)

    @classmethod
    @logging_time
    def get_tweet(cls, tweet_id, headers={}):
        return NetworkRequest.get(cls._get_url(f'/tweets/{tweet_id}'), headers=headers)

    @classmethod
    @logging_time
    def update_tweet(cls, tweet_id, data, headers={}):
        return NetworkRequest.put(cls._get_url(f'/tweets/{tweet_id}'), data, headers=headers)

    @classmethod
    @logging_time
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

def logging_time(func):
    def inner(*args, **kwargs):
        import time
        start = time.time()
        returnValue = func(*args, **kwargs)
        end = time.time()
        print(f'Function {func.__name__} took {end-start} seconds')
        return returnValue
    return inner

class Twitter:
    def __init__(self, username=None, password=None):
        self.auth = Auth(username, password)
    
    @retry_mechanism
    def list_tweets(self,skip=0,limit=100000000):
        return TwitterRequestHandler.list_tweets(skip,limit,headers={'Authorization': f'Bearer {self.auth.access_token}'})

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

class unique_checker:
    def __init__(self,items):
        
        self.unique = {item for item in items}
    def __enter__(self):
        return self
    def check(self, item):
        return item not in self.unique
    def add(self, item):
        self.unique.add(item)
    def __exit__(self, exc_type, exc_value, traceback):
        self.unique = set()
