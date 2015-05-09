class User (object):
    def __init__(self,user_id,screen_name,user_name=None,friends_count=None,followers_count=None,listed_count=None,Tweets_count=None,creation_time=None,creation_date=None,description=None,favourites_count=None):
        self.id = user_id
        self.screen_name = screen_name
        self.user_name = user_name
        self.friends_count = friends_count
        self.followers_count = followers_count
        self.listed_count = listed_count
        self.Tweets_count = Tweets_count
        self.creation_time = creation_time
        self.creation_date = creation_date
        self.description = description
        self.favourites_count = favourites_count
    
