from datetime import datetime
from messages import message
channel_id = 0

class Channel:
    def __init__(self, name, owner, is_private):
        global channel_id
        global users
        self.name = name
        self.owners = (dict(u_id = owners,
        first_name = users[owner].get_name_first,
        last_name = users[owners].get_name_last))
        self.members = ()
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

    def get_is_private(self):
        return self.is_private
    
    def send_message(self):
        curr_message 