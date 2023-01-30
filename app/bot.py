import os
import json
import tweepy

def main():
    # Get Twitter API credentials from environment variables
    consumer_key = os.environ["CONSUMER_KEY"]
    consumer_secret = os.environ["CONSUMER_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, tweet_mode='extended')

    # Open banned and supporter JSON files
    with open("banned.json", "r") as f:
        banned_ids = json.load(f)
    with open("supporters.json", "r") as f:
        supporter_ids = json.load(f)

    # Open last_seen_id JSON file
    with open("last_seen_id.json", "r") as f:
        last_seen_id = json.load(f)

    # Get tweets
    tweets = get_tweets(api, last_seen_id)

    # Retweet tweets
    retweet(api, tweets, banned_ids, supporter_ids)

    # Update last_seen_id
    with open("last_seen_id.json", "w") as f:
        json.dump(tweets[0].id, f)

def get_tweets(api, last_seen_id):
    query = "langtwt OR #langtwt"
    tweets = api.search(q=query, since_id=last_seen_id, tweet_mode='extended')
    return tweets

def retweet(api, tweets, banned_ids, supporter_ids):
    frequency = {}
    for tweet in tweets:
        if tweet.user.id in banned_ids:
            continue
        if tweet.user.id in supporter_ids:
            api.create_favorite(tweet.id)
        if tweet.user.id not in frequency:
            frequency[tweet.user.id] = 0
        if frequency[tweet.user.id] >= 2:
            continue
        api.retweet(tweet.id)
        frequency[tweet.user.id] += 1

if __name__ == "__main__":
    main()
