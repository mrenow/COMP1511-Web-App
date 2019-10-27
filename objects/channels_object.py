from datetime import datetime
from .messages import Message
from server.server import get_num_channels, inc_channels, get_users, get_channels, get_messages
'''
get_channels
'''


class Channel:
    def __init__(self, name, owner, is_public):
        self.name = name
        self.owners = set([owner])
        self.members = set([owner])
        self.is_public = is_public
        self.id = get_num_channels()
        
        self.message_list = []
        get_channels()[self.id] = self
        get_users()[owner].get_channels().add(self.id)
        get_users()[owner].get_owner_channels().add(self.id)
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
    def get_is_public(self):
        return self.is_public

    def get_id(self):
        return self.id

    def get_num_messages(self):
        return len(self.message_list)
    
    def send_message(self, message_obj):
        self.message_list.append(message_obj)
        return message_obj.get_id()
    

    def channel_messages(self, start, user):
        return [mess.to_json(user) for mess in self.message_list[-start-1:-start-51:-1]]

    def delete_message(self, message_id):
        for index, entry in enumerate(self.message_list):
            if message_id == entry.get_id():
                del self.message_list[index]
                return
        ValueError(f"delete_message: message {message_id} not found")
        
    def join(self, u_id):
        self.members.add(u_id)
        get_users()[u_id].get_channels().add(self.id) 


    def details(self):
        owner_members = []
        for x in self.owners:
            d = dict(u_id = get_users()[x].get_id(),
            first_name = get_users()[x].get_name_first(),
            last_name = get_users()[x].get_name_last())
            owner_members.append(d)
        
        members = []
        for x in self.members:
            d = dict(u_id = get_users()[x].get_id(),
            first_name = get_users()[x].get_name_first(),
            last_name = get_users()[x].get_name_last())   
            members.append(d)
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
        self.join(u_id)

    def remove_owner(self, u_id):
        self.owners.discard(u_id)

   

        
'''
owner = dict(u_id = owners,
        first_name = get_users()[owners].get_name_first,
        last_name = get_users()[owners].get_name_last)owner = dict(u_id = owners,
        first_name = get_users()[owners].get_name_first,
        last_name = get_users()[owners].get_name_last)
'''
