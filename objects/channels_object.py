from datetime import datetime, timedelta
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
        # Functions as the entire standup
        self._standup_message = None
        # Message list contains message_id
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

    def get_message_list(self):
        return self.message_list

    def get_num_messages(self):
        return len(self.message_list)
    
    def send_message(self, message_id):
        self.message_list.append(message_id)
        get_messages()[message_id].send()
        return message_id
    
    def standup_start(self, user, duration):
        if self.standup_active():
            raise ValueError(f"standup_start: Standup already active in channel {self.id}")

        # Overwrite old standup message with new unsent message.
        self._standup_message = Message("Standup results: \n", self.id, user, datetime.now() + timedelta(seconds = duration)).get_id()

    
    def standup_send(self, user, text):
        if not self.standup_active():
            raise ValueError(f"standup_send: No standup active in channel {self.id}")
        
        full_text = f"{get_users()[user].get_name_first()}: {text}\n"
        message = get_messages()[self._standup_message]

        # Append full_text to standup message.
        message.set_message(message.get_message() + full_text)

    '''
    Defines when a standup has ended. This is different to checking whether the sendtime is earlier than now
    as a 
    '''
    def standup_active(self):
        return self._standup_message != None and not get_messages()[self._standup_message].is_sent()

    '''
    Returns the completion datetime of the last standup initiated on the channel.
    Returns earliest possible time if no standup has been initiated.
    '''
    def standup_time(self):
        if self._standup_message == None:
            return datetime.min
        else:
            return get_messages()[self._standup_message].get_time()

    def channel_messages(self, start, user):    
        return [get_messages()[mess].to_json(user) for mess in self.message_list[-start-1:-start-51:-1]]

    def delete_message(self, message_id):
        for index, entry in enumerate(self.message_list):
            if message_id == entry:
                del self.message_list[index]
                return
        ValueError(f"delete_message: message {message_id} not found")
        
    def join(self, u_id):
        self.members.add(u_id)
        get_users()[u_id].get_channels().add(self.id) 


    def details(self):
        return dict(name = self.name,
                    owner_members = [get_users()[u_id].to_json() for u_id in self.owners],
                    all_members = [get_users()[u_id].to_json() for u_id in self.members])

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
