import os
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


class LangbotTest(unittest.TestCase):
  def test_checkProfile(self):
      # Check if thelangbot user id is correct
      self.assertEqual(api.get_user("thelangbot").id, 1389790399590506497)

  def test_checkRetweet(self):
    # Check if already retweeted a tweet
    try:
      api.retweet(1406685889925898248).message
    except tweepy.TweepError as e:
      self.assertEqual(e.reason,
            "[{'code': 327, 'message': 'You have already retweeted this Tweet.'}]")


if __name__ == '__main__':
    unittest.main()
