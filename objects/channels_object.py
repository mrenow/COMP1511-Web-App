from datetime import datetime
from messages import message
from server.server import Users, Channels
channel_id = 0

class Channel:
    def __init__(self, name, owner, is_private):
        global channel_id
        global Users
        global Channels
        self.name = name
        self.owners = set(owner)
        self.members = set()
        self.is_private = is_private
        self.id = channel_id
        channel_id += 1 
        self.message_list = []
        Channels[self.id] = self
        Users[owner].get_channels.add(self.id)


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
    
    def send_message(self, text, sender):
        curr_message = message(text, self.id, sender)
        self.message_list.append(curr_message)
        return curr_message.get_id()
        

    def delete_message(self, message_id):
        for x in self.message_list:
            if x.get_id == message_id:
                self.message_list.remove(x)
                break
    
    def join(self, u_id):
        self.members.add(u_id) 
        global Users
        Users[u_id].get_channels.add(self.channel_id) 

    def details(self):
        global Users
        for x in self.owners:
             = dict(u_id = x,
            first_name = Users[x].get_name_first(),
            last_name = Users[x].get_name_last())
        owner_members = []
        owner_members.append()

        for x in self.members:
             = dict(u_id = x,
            first_name = Users[x].get_name_first(),
            last_name = Users[x].get_name_last())   
        members = ()
        members.append()
        details = dict(name = self.name,
        owner_members = owner_members,
        members = members
        )

    def leave(self, u_id):
        global Users
        for x in self.members:
            if x == u_id:
                self.members.discard(x) 
        for x in self.owners:
            if x == u_id:
                self.owners.discard(x)
        Users[u_id].get_channels().discard(self.id)


    def add_owner(self, u_id):
        global Users
        self.owners.add(u_id)            
        Users[u_id].get_owners().add(self.id)

    def remove_owner(self, u_id):
        for x in self.owners:
            if x == u_id:
                self.owners.discard(x)

   

        
'''
owner = dict(u_id = owners,
        first_name = users[owners].get_name_first,
        last_name = users[owners].get_name_last)owner = dict(u_id = owners,
        first_name = users[owners].get_name_first,
        last_name = users[owners].get_name_last)
'''