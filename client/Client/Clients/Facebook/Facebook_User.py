class User(object):
    def __init__(self,user_id,user_name,category=None):
        self.id = user_id
        self.name = user_name
        self.category = category