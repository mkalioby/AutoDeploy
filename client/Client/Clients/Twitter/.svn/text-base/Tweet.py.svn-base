class Tweet(object):
    def __init__(self,crawl_id,tweet_id,User=None,text='',creation_time=None,creation_date=None,source=None,links=None,hashtags=None,mentions=None,in_reply_to_Tweet=None,in_reply_to_User=None,retweet_count=None,ontologies=None,entities=None,sentiment=None,retweeters=None):
        self.CrawlId = crawl_id
        self.id = tweet_id
        self.text = text
        self.creation_time = creation_time
        self.creation_date = creation_date
        self.source = source
        self.links = links
        if not(self.links == []):
            self.include_links = 1
        else:
            self.include_links = 0
        self.hashtags = hashtags
        self.ontologies = ontologies
        self.entities = entities
        self.sentiment = sentiment
        self.in_reply_to_Tweet = in_reply_to_Tweet
        self.in_reply_to_User = in_reply_to_User
        self.mentions = mentions
        if self.in_reply_to_Tweet or self.in_reply_to_User:
            self.is_reply = 1
        else:
            self.is_reply = 0
        if not(self.mentions == []) and not(self.is_reply == 1):
            self.is_mention = 1
        else:
            self.is_mention = 0
        self.retweet_count = retweet_count
        self.User = User
        self.retweeters = retweeters
        self.hour = 0
        if self.creation_time:
          self.hour = int(self.creation_time.split(":")[0])
