from multiprocessing import Lock

_users = {}  # u_id: user obj
_channels = {}  # chann
_messages = {}  # message_id: message obj

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
	return _num_messages


def num_users():
	return _user_count


def num_channels():
	return _num_channels


def channel_iter():
    return _channels.values()


def user_iter():
    return _users.values()


def message_iter():
    return _messages.values()


def get_channel(channel_id):
	"""
	Gets the channel with specified channel ID.
	Raises:
		ValueError: Channel ID does not exist in server.
	"""
	try:
		return _channels[channel_id]
	except KeyError:
		raise ValueError(f"Channel {channel_id} does not exist. channels: {_channels} in {__name__}")


def get_user(u_id):
	"""
	Gets the user with specified user ID.
	Raises:
		ValueError: User ID does not exist in server.
	"""
	try:
		return _users[u_id]
	except KeyError:
		raise ValueError(f"User {u_id} does not exist. users: {_users} in {__name__}")

def get_user_dictionary():
	global _users
	return _users
	
def get_message(message_id):
	"""
	Gets the message with specified message ID.
	Raises:
		ValueError: Messsge ID does not exist in server.
	"""
	try:
		return _messages[message_id]
	except KeyError:
		raise ValueError(f"Message {message_id} does not exist. messages: {_messages} in {__name__}")


def set_user(u_id, user_obj):
	_users[u_id] = user_obj


def set_channel(channel_id, channel_obj):
	_channels[channel_id] = channel_obj


def set_message(message_id, message_obj):
	_messages[message_id] = message_obj


def remove_channel(channel_id):
	"""
	Removes the specified channel from the server.
	Raises:
		ValueError: Messsge ID does not exist in server.
	"""
	try:
		del _channels[channel_id]
	except KeyError:
		raise ValueError(f"Channel {channel_id} does not exist. channels: {_channels}")


def remove_user(u_id):
	"""
	Removes the specified user from the server.
	Raises:
		ValueError: Messsge ID does not exist in server.
	"""
	try:
		del _users[u_id]
	except KeyError:
		raise ValueError(f"User {u_id} does not exist. users: {_users}")


def remove_message(message_id):
	"""
	Removes the specified message from the server.
	Raises:
		ValueError: Messsge ID does not exist in server.
	"""
	try:
		del _messages[message_id]
	except KeyError:
		raise ValueError(
			f"Message {message_id} does not exist. messages: {_messages}")


def get_unsent():
	return _unsent_messages


def lock_unsent():
    _unsent_lock.acquire()


def release_unsent():
    _unsent_lock.release()


def reset():
	global _users, _channels, _messages, _num_messages, _num_channels, _user_count
	_users = {}  # u_id: user obj
	_channels = {}  # chann
	_messages = {}  # message_id: message obj
	_num_messages = 0
	_num_channels = 0
	_user_count = 0
