import os
import tweepy
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup OAuth authentication for Tweepy
auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
# Rate limit = True: allows us to wait 15 minutes before retrying request
api = tweepy.API(auth, wait_on_rate_limit=True)


def main():
    """Like and retweet the most recent 100DaysOfLanguage related tweets"""
    
    query = "#100DaysOfLanguage OR 100daysoflanguage -filter:retweets -result_type:recent"

    for tweet in tweepy.Cursor(api.search, q=query).items(limit=300):
        try:
            # Retweet post
            print("\nRetweet Bot found tweet by @" +
                tweet.user.screen_name + ". " + "Attempting to retweet...")
            tweet.retweet()
            print("Tweet retweeted!")
            time.sleep(10)

        # Basic error handling - will print out why retweet failed to terminal
        except tweepy.TweepError as e:
            print(e.reason, "Tweet id: " + str(tweet.id))

        except StopIteration:
            print("Stopping...")
            break


if __name__ == "__main__":
    main()
