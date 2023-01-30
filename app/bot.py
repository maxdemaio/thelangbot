import tweepy
import json
from datetime import datetime, timedelta

# Set up your Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Load the banned and supporter JSON files
with open('data/banned.json', 'r') as file:
    banned_data = json.load(file)
with open('data/supporter.json', 'r') as file:
    supporter_data = json.load(file)

# Search for tweets with the #langtwt hashtag
now = datetime.now()
last_10_min = now - timedelta(minutes=10)
tweets = tweepy.Cursor(api.search_tweets,
                       q="#langtwt",
                       lang="en",
                       since_id=last_10_min.strftime("%Y-%m-%d"),
                       tweet_mode='extended').items(100)

# Keep track of the number of tweets from each user
user_tweet_count = {}

for tweet in tweets:
    # Don't retweet if the user is banned
    if tweet.user.id in banned_data['banned']:
        continue
    # Keep track of the number of tweets from this user
    if tweet.user.id in user_tweet_count:
        user_tweet_count[tweet.user.id] += 1
    else:
        user_tweet_count[tweet.user.id] = 1
    # Only retweet 2 tweets maximum from one user
    if user_tweet_count[tweet.user.id] > 2:
        continue
    # Retweet the tweet
    try:
        if tweet.user.id in supporter_data['supporters']:
            api.create_favorite(tweet.id)
        api.retweet(tweet.id)
        print(f"Retweeted tweet from {tweet.user.screen_name}")
    except tweepy.TweepError as e:
        print(f"Failed to retweet tweet from {tweet.user.screen_name}: {e}")
