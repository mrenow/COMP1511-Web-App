from datetime import datetime

channel_id = 0

class channel:
    def __init__(self, name, owner, is_private):
        self.name = name
        self.owners = set(owner)
        self.is_private = is_private
        self.id = channel_id
        channel_id += 1 
        self.message_list = []

    #messages(text,channel,time)
    def set_name(self, name):
        self.name = name
    
    def set_is_private(self, is_private):
        self.is_private = is_private
    
    def get_name(self):
        return self.name
    
    def get_owner(self):
        return self.owners

    def get_is_private():
        return is_private