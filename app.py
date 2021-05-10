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
    
    query = "#langtwt OR langtwt OR #100DaysOfLanguage OR 100daysoflanguage -filter:retweets -result_type:recent"
    newRetweets = 0 

    for tweet in tweepy.Cursor(api.search, q=query).items():
        # Breakpoint of 16 new retweets reached
        # 300 tweets / 3 hours limit --> 100 tweets / 1 hour
        # Server pings ever 10 minutes so we can do ~16 tweets every interval
        if newRetweets == 16:
            break

        try:
            # Retweet post
            print("\nRetweet Bot found tweet by @" +
                tweet.user.screen_name + ". " + "Attempting to retweet...")
            tweet.retweet()
            print("Tweet retweeted!")
            # Increment newly found retweet number
            newRetweets += 1
            time.sleep(5)

        # Basic error handling - will print out why retweet failed to terminal
        except tweepy.TweepError as e:
            print(e.reason, "Tweet id: " + str(tweet.id))
            print(e.api_code)
            if e.api_code == 185:
                print("Rate limit met, ending program")
                break

        except StopIteration:
            print("Stopping...")
            break
    
    print("Retweeted", newRetweets, "language tweets")
    

if __name__ == "__main__":
    main()
