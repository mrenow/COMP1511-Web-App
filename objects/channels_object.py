from datetime import datetime, timedelta
from .messages import Message
from server.server import get_num_channels, inc_channels, get_user, get_channel, get_message, set_user, set_message, set_channel, MAX_MESSAGE_LEN, STANDUP_START_STR, MAX_STANDUP_SECONDS 
'''
get_channels
'''


class Channel:
    def __init__(self, name_str, owner_id, is_public):
        self._name_str = name_str
        self._owners_set = set([owner_id])
        self._members_set = set([owner_id])
        self._is_public = is_public
        self._id = get_num_channels()

        # Functions as the entire standup
        self._standup_message_id = None
        # Message list contains message_id
        
        self._message_list = []
        set_channel(self._id,self)
        get_user(owner_id).get_channels().add(self._id)
        get_user(owner_id).get_owner_channels().add(self._id)
        inc_channels()

    def set_name(self, name_str):
        self._name_str = name_str
    
    def set_is_public(self, is_public):
        self._is_public = is_public
    
    def get_name(self):
        return self._name_str
    
    def get_owners(self):
        return self._owners_set
    def get_members(self):
        return self._members_set
    def get_is_public(self):
        return self._is_public

    def get_id(self):
        return self._id

    def get_message_list(self):
        return self._message_list

    def get_num_messages(self):
        return len(self._message_list)
    
    def send_message(self, message_id):
        self._message_list.append(message_id)
        get_message(message_id).send()
        return message_id
    
    def standup_start(self, u_id, seconds):
        if self.standup_active():
            raise ValueError(f"Standup already active in channel {self._name_str}.")
        if seconds > MAX_STANDUP_SECONDS:
            raise ValueError(f"Standup duration ({seconds}s) exceeds maximum ({MAX_STANDUP_SECONDS}s).")

        # Overwrite old standup message with new unsent message.
        time_finish = datetime.now() + timedelta(seconds = seconds)
        self._standup_message_id = Message(STANDUP_START_STR, self._id, u_id, time = time_finish, is_standup = True).get_id()
        
        return time_finish
    
    
    def standup_send(self, u_id, text):
        if not self.standup_active():
            raise ValueError(f"No standup active in channel {self._name_str}")
        if MAX_MESSAGE_LEN < len(text):
            raise ValueError(f"Message '{text[:10]}...' with length {len(text)} exceeds maximum allowable length {MAX_MESSAGE_LEN}.")
        
        full_text = f"\n{get_user(u_id).get_name_first()}: {text}"
        message = get_message(self._standup_message_id)

        # Append full_text to standup message.
        message.set_message(message.get_message() + full_text)

    '''
    Defines when a standup has ended. This is different to checking whether the sendtime is earlier than now
    as a 
    '''
    def standup_active(self):
        return self._standup_message_id != None and not get_message(self._standup_message_id).is_sent()

    '''
    Returns the completion datetime of the last standup initiated on the channel.
    Returns earliest possible time if no standup has been initiated.
    '''
    def standup_time(self):
        if self._standup_message_id == None:
            return datetime.min
        else:
            return get_message(self._standup_message_id).get_time()

    def channel_messages(self, start, u_id):    
        return [get_message(mess).to_json(u_id) for mess in self._message_list[-start-1:-start-51:-1]]

    def delete_message(self, message_id):
        for index, entry in enumerate(self._message_list):
            if message_id == entry:
                del self._message_list[index]
                return
        ValueError(f"delete_message: message {message_id} not found")
        
    def join(self, u_id):
        self._members_set.add(u_id)
        get_user(u_id).get_channels().add(self._id) 


    def details(self):
        return dict(name_str = self._name_str,
                    owner_members = [get_user(u_id).to_json() for u_id in self._owners_set],
                    all_members = [get_user(u_id).to_json() for u_id in self._members_set])

    def leave(self, u_id):
        self._members_set.discard(u_id)
        if u_id in self._owners_set:
            self._owners_set.discard(u_id)
        get_user(u_id).get_channels().discard(self._id)


    def add_owner(self, u_id):
        self._owners_set.add(u_id)          
        get_user(u_id).get_channels().add(self._id)
        self.join(u_id)

    def remove_owner(self, u_id):
        self._owners_set.discard(u_id)

   

        
'''
owner_id = dict(u_id = owners,
        first_name = get_user(owners).get_name_first,
        last_name = get_user(owners).get_name_last)owner_id = dict(u_id = owners,
        first_name = get_user(owners).get_name_first,
        last_name = get_user(owners).get_name_last)
'''
