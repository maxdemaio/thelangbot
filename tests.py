import os
import tweepy
import time
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


class TweepyTest(unittest.TestCase):
  def test_checkProfile(self):
      # Check if thelangbot user id is correct
      self.assertEqual(api.get_user("thelangbot").id, 1389790399590506497)




if __name__ == '__main__':
    unittest.main()
