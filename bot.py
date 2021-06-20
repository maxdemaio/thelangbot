import os
import tweepy
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

""" 
Dev NOTE: For testing purposes set the items(limit=3) to only get three tweets and test.
Also the logs will have the most recent tweet ID if needed / can check Twitter web.
"""

# Setup OAuth authentication for Tweepy
auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
# Rate limit = True: allows us to wait 15 minutes before retrying request
api = tweepy.API(auth, wait_on_rate_limit=True)
# Setup file to store last tweet retweeted
fileName = "lastSeenId.txt"


def retrieveLastSeenId(fileName):
    fRead = open(fileName, 'r')
    lastSeenId = int(fRead.read().strip())
    fRead.close()
    return lastSeenId


def storeLastSeenId(lastSeenId, fileName):
    fWrite = open(fileName, 'w')
    fWrite.write(str(lastSeenId))
    fWrite.close()
    return


def retweet(myQuery):
    """Retweet tweets from the specified query"""
    # Obtain last seen tweet
    lastSeenId = retrieveLastSeenId(fileName)
    print("Last seen tweet: " + str(lastSeenId) + "\n", flush=True)
    i = 0

    for tweet in tweepy.Cursor(api.search, since_id=lastSeenId, q=myQuery).items():
        try:
            # Retweet post
            print("Retweet Bot found tweet by @" +
                  tweet.user.screen_name + ". " + "Attempting to retweet...", flush=True)
            tweet.retweet()
            print(tweet.text, flush=True)
            print("Tweet retweeted!", flush=True)

            # Update last seen tweet with the newest tweet (top of list)
            if (i == 0):
                currLastSeenId = tweet.id
                storeLastSeenId(currLastSeenId, fileName)
                print("Updating last seen tweet to: " +
                    str(currLastSeenId) + "\n", flush=True)
            i += 1
            time.sleep(5)

        # Basic error handling - will print out why retweet failed to terminal
        except tweepy.TweepError as e:
            print(e.reason, "Tweet id: " + str(tweet.id), flush=True)
            if e.api_code == 185:
                print("Rate limit met, ending program", flush=True)
                break

        except StopIteration:
            print("Stopping...", flush=True)
            break



if __name__ == "__main__":
    retweet("#langtwt OR langtwt OR #100DaysOfLanguage OR 100daysoflanguage -filter:retweets -result_type:recent")
