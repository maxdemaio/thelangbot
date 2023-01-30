import os
import json
import tweepy

def main():
    # Get Twitter API credentials from environment variables
    consumer_key = os.environ["API_KEY"]
    consumer_secret = os.environ["API_SECRET_KEY"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_SECRET"]

    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Rate limit = True: allows us to wait 15 minutes before retrying request
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Open banned and supporter JSON files
    with open("data/banned.json", "r") as f:
        banned_ids = json.load(f)
    with open("data/supporters.json", "r") as f:
        supporter_ids = json.load(f)

    # Open last_seen_id JSON file
    with open("data/last_seen_id.json", "r") as f:
        last_seen_id = json.load(f)

    # Get tweets
    tweets = get_tweets(api, last_seen_id)

    # Retweet tweets
    retweet(api, tweets, banned_ids, supporter_ids)

    # Update last_seen_id
    print("Updating last seen tweet to: " +
        str(tweets[0].id) + "\n", flush=True)
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
        print("thelangbot found tweet by @" + 
                    tweet.user.screen_name + ". " + "Attempting to retweet...", flush=True)
        api.retweet(tweet.id)
        print(tweet.text, flush=True)
        print("Tweet retweeted!", flush=True)

        frequency[tweet.user.id] += 1

if __name__ == "__main__":
    main()
