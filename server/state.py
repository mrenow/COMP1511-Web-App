from multiprocessing import Lock

_users = {} # u_id: user obj
_channels = {} # chann
_messages = {} # message_id: message obj

_unsent_lock = Lock()
_unsent_messages = [] 

active_standup = False

_num_messages = 0
_user_count = 0
_num_channels = 0

def inc_users():
	global _user_count
	_user_count += 1

def inc_channels():
	global _num_channels
	_num_channels += 1

def inc_messages():
	global _num_messages
	_num_messages += 1

def num_messages():
	global _num_messages
	return _num_messages
def num_users():
	global _user_count
	return _user_count
def num_channels():
	global _num_channels
	return _num_channels
def channel_iter():
    return _channels.values()
def user_iter():
    return _users.values()
def message_iter():
    return _messages.values()
def get_channel(channel_id):
	try:
		return _channels[channel_id]
	except(KeyError):
		raise ValueError(f"Channel {channel_id} does not exist. channels: {_channels} in {__name__}")
	
def get_user(u_id):
	try:
		return _users[u_id]
	except(KeyError):
		raise ValueError(f"User {u_id} does not exist. users: {_users} in {__name__}")

def get_message(message_id):
	try:
		return _messages[message_id]
	except(KeyError):
		raise ValueError(f"Message {message_id} does not exist. messages: {_messages} in {__name__}")

def set_user(u_id, user_obj):
	global _users
	_users[u_id] = user_obj

def set_channel(channel_id, channel_obj):
	global _channels
	_channels[channel_id] = channel_obj

def set_message(message_id, message_obj):
	global _messages
	_messages[message_id] = message_obj

def remove_channel(channel_id):
	try:
		del _channels[channel_id]
	except(KeyError):
		raise ValueError(f"Channel {channel_id} does not exist. channels: {_channels}")
	
def remove_user(u_id):
	try:
		del _users[u_id]
	except(KeyError):
		raise ValueError(f"User {u_id} does not exist. users: {_users}")

def remove_message(message_id):
	try:
		del _messages[message_id]
	except(KeyError):
		raise ValueError(f"Message {message_id} does not exist. messages: {_messages}")
	

def get_unsent():
	global _unsent_messages
	return _unsent_messages
    
def lock_unsent():
    _unsent_lock.acquire()
def release_unsent():
    _unsent_lock.release()

def reset():
	global _users, _channels, _messages, _num_messages, _num_channels, _user_count
	_users = {} # u_id: user obj
	_channels = {} # chann
	_messages = {} # message_id: message obj
	_num_messages = 0
	_num_channels = 0
	_user_count = 0
