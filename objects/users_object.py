from server.server import channels, users
user_count = 0

class User:

    def __init__(self, name_first, name_last, email, u_id):
        global user_count
        self._u_id = u_id
        self._name_first = name_first
        self._name_last = name_last
        self._email = email
        self._handle_str = name_first + name_last
        self._profile_picture = None
        self._channels = set()
        self._admin_channels = set()
        self._owner_channels = set()
        user_count += 1

    def get_name_first(self, user):
        return self._name_first

    def set_name_first(self, user, name_first):
        self._name_first = name_first

    def get_name_last(self, user):
        return self._name_last

    def set_name_last(self, user, name_last):
        self._name_last = name_last
    
    def get_email(self, user):
        return self._email

    def set_email(self, user, email):
        self._email = email

    def get_channels(self, user):
        return self._channels

    def get_admin_channels(self, user):
        return self._admin_channels
    
    def get_owner_channels(self, user):
        return self._owner_channels
    
    def add_channel(self, user, channel_id):
        global channels
        self._channels[channel_id] = channels[channel_id]

    def add_admin_channel(self, user, channel_id):
        global channels
        self._admin_channels[channel_id] = channels[channel_id]

    def add_owner_channel(self, user, channel_id):
        global channels
        self._owner_channels[channel_id] = channels[channel_id]

    def get_handle_str(self, user):
        return self._handle_str

    def set_handle_str(self, user, handle_str):
        self._handle_str = handle_str

    def get_user_profile(self, user):
        return dict(email = self._email, 
                    name_first = self._name_first, 
                    name_last = self._name_last,
                    handle_str = self._handle_str)
    
    def to_json(self, user):
        return dict(u_id = self._u_id, 
                    name_first = self._name_first, 
                    name_last = self._name_last)


