import os
import mysql.connector
import tweepy
import unittest
from bot import retweet

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



class LangbotTest(unittest.TestCase):
  def test_checkValidProfile(self):
      # Check if thelangbot user id is correct
      self.assertEqual(api.get_user("thelangbot").id, 1389790399590506497)

  def test_checkInvalidRetweet(self):
    # Check if already retweeted a tweet
    try:
      api.retweet(1406685889925898248)
    except tweepy.TweepError as e:
      self.assertEqual(e.reason,
            "[{'code': 327, 'message': 'You have already retweeted this Tweet.'}]")

  def test_checkValidPatron(self):
    # Check if user is a patron
    mycursor.execute(
        "SELECT * FROM patreon WHERE twitterUser = %s", ("maxwelldemaio",))
    myresult = mycursor.fetchall()
    self.assertEqual(len(myresult), 1)



if __name__ == '__main__':
    unittest.main()
    mycursor.close()
    mydb.close()
    print("Test cases finished")
