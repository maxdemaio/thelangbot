import pytest
from bot2 import *

def test_retweet():
    # Test that the retweet function retweets a tweet
    tweet = {"id": 1, "user": {"id": 2}}
    assert retweet(tweet) == True

def test_dont_retweet_banned():
    # Test that the retweet function does not retweet a tweet from a banned user
    banned_users = [2]
    tweet = {"id": 1, "user": {"id": 2}}
    assert retweet(tweet, banned_users) == False

def test_like_and_retweet_supporter():
    # Test that the retweet function likes and retweets a tweet from a supporter user
    supporter_users = [2]
    tweet = {"id": 1, "user": {"id": 2}}
    assert retweet(tweet, supporter_users) == True

def test_limit_retweets_per_user():
    # Test that the retweet function limits the number of retweets from one user
    tweets = [{"id": 1, "user": {"id": 2}}, {"id": 2, "user": {"id": 2}}, {"id": 3, "user": {"id": 2}}]
    assert retweet(tweets, max_per_user=2) == False
