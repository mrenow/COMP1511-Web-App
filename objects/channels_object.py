from datetime import datetime
from .messages import Message
from server.server import get_num_channels, inc_channels, get_users, get_channels, get_messages
'''
get_channels
'''


class Channel:
    def __init__(self, name, owner, is_private):
        self.name = name
        self.owners = set([owner])
        self.members = set()
        self.is_private = is_private
        self.id = get_num_channels()
        
        self.message_list = []
        get_channels()[self.id] = self
        inc_channels()


    def set_name(self, name):
        self.name = name
    
    def set_is_private(self, is_private):
        self.is_private = is_private
    
    def get_name(self):
        return self.name
    
    def get_owners(self):
        return self.owners
    def get_members(self):
        return self.members
    def get_is_private(self):
        return self.is_private

    def get_id(self):
        return self.id
    
    def send_message(self, text, sender):
        curr_message = Message(text, self.id, sender)
        self.message_list.append(curr_message)
        return curr_message.get_id()
        
    def channel_messages(self, start, user):
        return [mess.to_json(user) for mess in self.message_list[-start-1:-start-51:-1]]

    def delete_message(self, message_id):
        # Raises value if messages_id is not in list.
        self.message_list.remove(message_id)
    
    def join(self, u_id):
        self.members.add(u_id)
        get_users()[u_id].get_channels().add(self.id) 

    def details(self):
        owner_members = []
        for x in self.owners:
            d = dict(u_id = x,
            first_name = get_users()[x].get_name_first(),
            last_name = get_users()[x].get_name_last())
            owner_members.append()
        

        for x in self.members:
            d = dict(u_id = x,
            first_name = get_users()[x].get_name_first(),
            last_name = get_users()[x].get_name_last())   
        members = []
        members.append()
        details = dict( name = self.name,
                        owner_members = owner_members,
                        members = members)
        return details

    def leave(self, u_id):
        self.members.discard(u_id)
        if u_id in self.owners:
            self.owners.discard(u_id)
        get_users()[u_id].get_channels().discard(self.id)


    def add_owner(self, u_id):
        self.owners.add(u_id)          
        get_users()[u_id].get_channels().add(self.id)

    def remove_owner(self, u_id):
        self.owners.discard(u_id)

   

        
'''
owner = dict(u_id = owners,
        first_name = get_users()[owners].get_name_first,
        last_name = get_users()[owners].get_name_last)owner = dict(u_id = owners,
        first_name = get_users()[owners].get_name_first,
        last_name = get_users()[owners].get_name_last)
'''
