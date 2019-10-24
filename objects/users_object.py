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
        user_count += 1

    def get_name_first(self, user):
        return self._name_first

    def get_name_last(self, user):
        return self._name_last

    def get_email(self, user):
        return self._email

    def set_user_profile(self, name_first, name_last):
        pass
    
    
    def get_user_profile(self, user):
        return self._email, self._name_first, self._name_last, self._handle_str
    
    def to_json(self, user):
        return dict(u_id = self._u_id, 
                    name_first = self._name_first, 
                    name_last = self._name_last)


