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
    retweet(api, tweets, banned_ids, supporter_ids, last_seen_id)

    # Update last_seen_id
    print("Updating last seen tweet to: " +
        tweets[0].id_str + "\n", flush=True)
    with open("last_seen_id.json", "w") as f:
        json.dump(tweets[0].id_str, f)

def get_tweets(api, last_seen_id):
    query = "#langtwt OR #100DaysOfLanguage exclude:retweets"
    tweets = api.search(q=query, since_id=last_seen_id, tweet_mode='extended')
    return tweets

def retweet(api, tweets, banned_ids, supporter_ids, last_seen_id):
    frequency = {}
    for tweet in tweets:
        if tweet.id_str == last_seen_id["last_seen_id"]:
            continue
        if tweet.user.id_str in banned_ids["banned"]:
            continue
        if tweet.user.id_str in supporter_ids["supporters"]:
            api.create_favorite(tweet.id)
        if tweet.user.id_str not in frequency:
            frequency[tweet.user.id] = 0
        if frequency[tweet.user.id] >= 2:
            continue
        print("thelangbot found tweet by @" + tweet.user.screen_name + ". " + "Attempting to retweet...", file=sys.stderr, flush=True)
        print("User ID is: " + tweet.user.id_str, file=sys.stderr, flush=True)
        api.retweet(tweet.id)
        print("Tweet retweeted!", file=sys.stderr, flush=True)

        frequency[tweet.user.id] += 1

if __name__ == "__main__":
    main()
