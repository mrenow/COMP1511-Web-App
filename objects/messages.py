from datetime import datetime
from server.server import messages


# { react_id, u_ids, is_this_user_reacted } 
next_id = 0
MAX_LEN = 1000
class message:

    def __init__(self, text, channel, sender, time = datetime.now()):
        global next_id, messages
        if MAX_LEN < text:
            raise ValueError(f"message.__init__: '{text[:10]}...' exceeds maximum allowable length.") 
        self._message = text
        self._u_id = sender
        self._time_created = time
        self._is_sent = time <= datetime.now()
        self._message_id = next_id
        self._is_pinned = False
        self._reacts = {} # Dictionary of react id: react object.
        next_id += 1
        messages[self._u_id] = self 

    
    def get_time(self):
        return self._time_created
    
    def get_id(self):
        return self._message_id
    
    def is_sent(self):
        return self._is_sent

    def is_pinned(self):
        return self._is_pinned

    def pin(self, user):
        if self._is_pinned:
            raise ValueError(f"message.pin: Message {self._message_id} '{self._message[:10]}...' is already pinned.")
        else:
            self._is_pinned = True

    def unpin(self, user):
        if self._is_pinned:
            raise ValueError(f"message.unpin: Message {self._message_id} '{self._message[:10]}...' is not pinned.")
        else:
            self._is_pinned = False

    def add_react(self, user, react):
        if react in self._reacts and user in self._reacts.get(react)._u_ids:
            raise ValueError(f"message.add_react: User {user} already has react_id {react} on message {self._message_id}: '{self._message[:10]}...'")
        elif react not in self._reacts:
            self._reacts = react(react, user)
        else:
            self._reacts.get(react)._u_ids.append(user)

    def remove_react(self, user, react):
        if react not in self._reacts or user not in self._reacts.get(react)._u_ids:
            raise ValueError(f"message.remove_react: User {user} already has react_id {react} on message {self._message_id}: '{self._message[:10]}...'")
        else:
            self._reacts.get(react)._u_ids.remove(user)
            if not self._reacts.get(react):
                del self._reacts[react]

    # Returns the reacts list as in specification
    def get_reacts(self, user): 
        return [react.details(user) for react in self._reacts.values()]

    def to_json(self, user):
        return dict(message_id = self._message_id,
                    u_id = self._u_id,
                    message = self._message,
                    time_created  = self._time_created,
                    reacts = self.get_reacts(user),
                    is_pinned = self._is_pinned)
class react:
    def __init__(self, id, user):
        self._u_ids = set(user)
        self._react_id = id

    def to_json(self, user):
        return dict(u_ids = list(self._u_ids),
                    react_id = self._react_id,
                    is_this_user_reacted = (user in self._u_ids))

if __name__ == "__main__":
    pass


    

