import os, mysql.connector, time, tweepy
from utils import Utils


def main(tweets: list, mydb, mycursor, lastSeenId: int) -> None:
    # Setup current last seen tweet to be the previous one
    # This is just in case there are no items in the iterator
    currLastSeenId: int = lastSeenId

    # Setup tweeters frequency map for rate limit
    tweeters: dict[str, int] = {}

    blackList: set = Utils.getBlacklist(mycursor)
    supporters: set = Utils.getSupporters(mycursor)
    
    for tweet in tweets:
        try:
            twitterUser: str = tweet.user.screen_name
            
            #Skip if user in blacklist
            if twitterUser in blackList:
                print("Blacklisted tweet by - @" + twitterUser, flush=True)
                continue
        
            # Add to frequency map
            if twitterUser not in tweeters:
                tweeters[twitterUser] = 1
            else:
                tweeters[twitterUser] += 1
        
            # Make sure they have not met rate limit of 2 tweets per 10 minutes
            if tweeters[twitterUser] <= 2:
                # Like tweet if supporter
                if twitterUser in supporters:
                    tweet.favorite()
                    print("Liking tweet by" + twitterUser, flush=True)

                # Retweet post
                print("Retweet Bot found tweet by @" + 
                    twitterUser + ". " + "Attempting to retweet...", flush=True)
                tweet.retweet()
                print(tweet.text, flush=True)
                print("Tweet retweeted!", flush=True)

            # Update last seen tweet with the newest tweet (bottom of list)
            currLastSeenId = tweet.id
            time.sleep(5)

        # Basic error handling - will print out why retweet failed to terminal
        except tweepy.TweepError as e:
            print(e.reason, "Tweet id: " + str(tweet.id), flush=True)
            if e.api_code == 185:
                print("Rate limit met, ending program", flush=True)
                break

        except Exception:
            print("Stopping due to exception...", flush=True)
            break
    
    # After iteration, store the last seen tweet id (newest)
    # Only store if it is different
    if(lastSeenId != currLastSeenId):
        Utils.storeLastSeenId(mydb, mycursor, currLastSeenId)
        print("Updating last seen tweet to: " +
        str(currLastSeenId) + "\n", flush=True)

    return

    

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Setup OAuth authentication for Tweepy
    auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
    # Rate limit = True: allows us to wait 15 minutes before retrying request
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Setup MySQL db
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_DB"))
    mycursor = mydb.cursor()

    # Set up tweets from api
    # Only select tweets from our query and since our last seen tweet
    # Reverse the generator (which is an iterator, all generators are iterators, all iterators are iterables)
    # This makes the tweets ordered from oldest -> newest
    # Obtain last seen tweet
    lastSeenId: int = Utils.retrieveLastSeenId(mycursor)
    print("Last seen tweet: " + str(lastSeenId) + "\n", flush=True)
    myQuery: str = "#langtwt OR #100DaysOfLanguage OR 100daysoflanguage -filter:retweets -result_type:recent"
    tweets = reversed(list(tweepy.Cursor(api.search, since_id=lastSeenId, q=myQuery).items()))

    main(tweets, mydb, mycursor, lastSeenId)
    mycursor.close()
    mydb.close()
    print("\nRetweet function completed and db connection closed", flush=True)
