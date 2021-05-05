import os
import tweepy
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))

api = tweepy.API(auth, wait_on_rate_limit=True)
user = api.me()

print(user)