from server.server import channels, users, OWNER, ADMIN, MEMBER
user_count = 0

class User:

    def __init__(self, name_first, name_last, email, password):
        global user_count
        self._u_id = user_count
        self._password = password
        self._name_first = name_first
        self._name_last = name_last
        self._email = email
        if user_count == 0:
            self._permission_id = ADMIN
        else:
            self._permission_id = MEMBER
        self._handle_str = name_first + name_last
        self._profile_picture = None
        self._channels = set()
        self._admin_channels = set()
        self._owner_channels = set()
        users[self._u_id] = self
        user_count += 1

    def get_id(self):
        return self._u_id
        
    def get_name_first(self):
        return self._name_first

    def set_name_first(self, name_first):
        self._name_first = name_first

    def get_name_last(self):
        return self._name_last

    def set_name_last(self, name_last):
        self._name_last = name_last
    
    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email
    def get_permission():
        return self._permission_id


    def get_channels(self):
        return self._channels

    def get_admin_channels(self):
        return self._admin_channels
    
    def get_owner_channels(self):
        return self._owner_channels
    
    def add_channel(self, channel_id):
        global channels
        self._channels[channel_id] = channels[channel_id]

    def add_admin_channel(self,  channel_id):
        global channels
        self._admin_channels[channel_id] = channels[channel_id]

    def add_owner_channel(self,  channel_id):
        global channels
        self._owner_channels[channel_id] = channels[channel_id]

    def get_handle_str(self):
        return self._handle_str

    def set_handle_str(self, handle_str):
        self._handle_str = handle_str

    def get_user_profile(self):
        return dict(email = self._email, 
                    name_first = self._name_first, 
                    name_last = self._name_last,
                    handle_str = self._handle_str)
    
    def to_json(self):
        return dict(u_id = self._u_id, 
                    name_first = self._name_first, 
                    name_last = self._name_last)


