import os
import tweepy
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))

# Rate limit= true: allows us to wait 15 minutes before retrying request
api = tweepy.API(auth, wait_on_rate_limit=True)
user = api.me()

# Gather search terms for #100DaysOfLanguage
search = "LanguageLearning"
numOfTweets = 500

for tweet in tweepy.Cursor(api.search, search).items(numOfTweets):
    try:
        tweet.favorite()
        print("Tweet liked")
        tweet.retweet()
        print("Tweet retweeted")
        time.sleep(10)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
