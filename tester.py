# A tester for testing functionality of the bot in a local environment or on a server.
# Database functionality is optional. If databases are being used, the databases are not updated by default.

import os, importlib, time
from mocks import mock_t
import traceback

mydb = None
mycursor = None

#Checks to see if the mysql module is installed and, when it is, the database and cursor are initialized. 
def setupDb() -> None:
    mysql = None
    try:
        mysql = importlib.import_module("mysql.connector")
    except:
        print(traceback.format_exc(), flush=True)
        return
        
    global mydb, mycursor
    
    try:
        mydb = mysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_DB"))
        mycursor = mydb.cursor()
    except:
        print(traceback.format_exc(), flush=True)
        

def getBlacklist() -> set:
    if mycursor == None:
        return set([])

    try:
        mycursor.execute(
            "SELECT * FROM blacklist")
        myresult = mycursor.fetchall()
        usernames = set([row[0] for row in myresult])
        return usernames
    except:
        print(traceback.format_exc(), flush=True)
        return set([])
        
def getSupporters() -> set:
    if mycursor == None:
        return set([])

    try:
        mycursor.execute(
            "SELECT * FROM supporter")
        myresult = mycursor.fetchall()
        usernames = set([row[0] for row in myresult])
        return usernames
    except:
        print(traceback.format_exc(), flush=True)
        return set([])
        
def retrieveLastSeenId() -> int:
    if mycursor == None:
        return 0

    try:
        mycursor.execute("SELECT * FROM tweet")
        myresult = mycursor.fetchall()
        return myresult[0][1]
    except:
        print(traceback.format_exc(), flush=True)
        return 0


def storeLastSeenId(lastSeenId: int) -> None:
    if mycursor == None:
        return

    try:
        exampleId: int = (lastSeenId)
        mycursor.execute("UPDATE tweet SET tweetId = '%s' WHERE id = 1", (exampleId,))
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected", flush=True)

    except:
        print(traceback.format_exc(), flush=True)

    return

#By default, databases are not updated.
def main(tweets : list, updateDB = False) -> None:
    # Obtain last seen tweet
    lastSeenId: int = retrieveLastSeenId()
    print("Last seen tweet: " + str(lastSeenId) + "\n", flush=True)

    # Setup current last seen tweet to be the previous one
    # This is just in case there are no items in the iterator
    currLastSeenId: int = lastSeenId

    # Setup tweeters frequency map for rate limit
    tweeters: dict[str, int] = {}

    # Get blacklist here
    blackList : set = getBlacklist()
        
    # Get supporters here
    supporters : set = getSupporters()
        
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

        except StopIteration:
            print("Stopping...", flush=True)
            break
        
        except Exception:
            print(traceback.format_exc(), "Tweet id: " + str(tweet.id), flush=True)


    # After iteration, store the last seen tweet id (newest)
    # Only store if it is different and updateDB == True
    if(updateDB == True and lastSeenId != currLastSeenId):
        storeLastSeenId(currLastSeenId)
        print("Updating last seen tweet to: " +
        str(currLastSeenId) + "\n", flush=True)

    return


if __name__ == "__main__":
    setupDb()

    mock_t_list = [mock_t("user", "I study English."),
                mock_t("user", "I study Japanese."),
              mock_t("user", "I study Korean."),
              ]
    
    main(mock_t_list)
    
    if mycursor != None:
        mycursor.close()
    if mydb != None:
        mydb.close()
        
    print("\nRetweet function completed and db connection closed", flush=True)
