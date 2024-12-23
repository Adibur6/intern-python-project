
from util import Twitter,TwitterRequestHandler
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
jokes = {joke['text'] for joke in twitter.list_tweets()['body']}
print('Getting latest tweets....\n')
lastest_tweets = twitter.list_tweets(skip=0,limit=5)['body']
for tweet in lastest_tweets:
    print(f"{tweet['author']['username']} |||| {tweet['created_at']}\n{tweet['text']}\n")
i=0
while i < 10:
    joke = pyjokes.get_joke()
    if joke not in jokes:
        print(f"Posting tweet:\n{joke}")
        twitter.create_tweet({'text': joke})
        jokes.add(joke)
        i += 1
        time.sleep(1)
    

