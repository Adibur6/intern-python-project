
from util import Twitter,TwitterRequestHandler, unique_checker
import pyjokes
import time


response = TwitterRequestHandler.create_user({
    'username': 'adib',
    'password': '1234',
    'firstname': 'Adib',
    'lastname': 'Firman'
})
if response['code'] == 500:
    print('User already exists')
else:
    print('User created')

print("User login....")
twitter = Twitter('adib', '1234')


print('Getting latest tweets....\n')
lastest_tweets = twitter.list_tweets(skip=0,limit=5)['body']


for tweet in lastest_tweets:
    print(f"{tweet['author']['username']} |||| {tweet['created_at']}\n{tweet['text']}\n")

print(twitter.list_tweets()['body'])

with unique_checker([joke['text'] for joke in twitter.list_tweets()['body']]) as jokes:
    i=0
    twitter.list_tweets()
    while i < 10:
        joke = pyjokes.get_joke()
        if jokes.check(joke):
            print(f"Posting tweet:\n{joke}")
            twitter.create_tweet({'text': joke})
            jokes.add(joke)
            i += 1
            time.sleep(1)
    

