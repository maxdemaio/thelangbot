import os, unittest
import bot
from mocks import mock_t

from unittest.mock import MagicMock
import tweepy

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup OAuth authentication for Tweepy
auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
# Rate limit = True: allows us to wait 15 minutes before retrying request
api = tweepy.API(auth, wait_on_rate_limit=True)

# Setup Mock MySQL db
# Due to None type we won't actually hit the DB
mydb = None
mycursor = None


class LangbotTests(unittest.TestCase):
  def test_validApiProfileCheck(self):
      # Check if thelangbot user id is correct
      self.assertEqual(api.get_user("thelangbot").id, 1389790399590506497)

  def test_validUtilSupporter(self):
    # Mock the Util supporter method (don't change it's return value)
    # Call blacklist Util method
    # assert that it returns a set
    return

  def test_validUtilBlacklist(self):
    # Mock the Util blacklist method (don't change it's return value)
    # Call blacklist Util method
    # assert that it returns a set
    return

  def test_validRetweets(self):
    # Given list of Mock tweets
    mock_t_list = [mock_t("user", "I study English."),
                    mock_t("user", "I study Japanese."),
                  mock_t("user", "I study Korean."),
                  ]
    # When we call api to return our list of tweets
    # Mock response
    bot.main(mock_t_list, mydb, mycursor, 0)

    # Then assert we get the "Tweets retweeted" status for each tweet
    return

if __name__ == '__main__':
    unittest.main(exit=False)
    if mycursor != None:
        mycursor.close()
    if mydb != None:
        mydb.close()
