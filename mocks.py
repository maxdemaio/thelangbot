'''
These classes are used to mimic some of the behavior of tweets obtained using the tweepy library (found at https://github.com/tweepy/tweepy) in order
to perform functionality tests in a local environment.
'''

#Counts the number of mock_t objects to assign each one an id.
mock_t_count = 0

class mock_user():
    def __init__(self, screen_name = ""):
        self.screen_name = screen_name if type(screen_name) == str else ""
        
class mock_t ():
    def __init__(self, screen_name = "", text = ""):
        global mock_t_count
        mock_t_count+=1
        self.id = mock_t_count
        self.user = mock_user(screen_name) 
        self.text = text if type(text) == str else ""
        
    def retweet(self):
        print("Retweeted.")

    def favorite(self):
        print("Favorited")
