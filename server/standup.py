from datetime import datetime, timedelta
from server.AccessError import AccessError
from server.constants import *
from server.state import *
from server.auth_util import *
from server.export import export
@export("/standup/start", methods=["POST"])
@authorise
def standup_start(client_id, channel_id, length):
	"""Commences standup
	
	For a given channel, start the standup period whereby for the next "length" seconds 
	if someone calls "standup_send" with a message, it is buffered during the X second window 
	then at the end of the X second window a message will be added to the message queue in 
	the channel from the user who started the standup. X is an integer that denotes 
	the number of seconds that the standup occurs for

	Args: 
		token: A str used to identify and verify a user
		channel_id: An int used to identify a specific channel
		length: An int representing the number of seconds the standup occurs for

	Returns:
		time_finish: A timestamp of when standup will finish

	Raises:
		ValueError: Channel ID is not a valid channel
		ValueError: An active standup is currently running in this channel
	"""
	authcheck(client_id, channel_id=channel_id)
	# Raises an error if standup already active
	time_finish = get_channel(channel_id).standup_start(client_id, length)
	return {"time_finish": time_finish}


@export("/standup/active", methods=["GET"])
@authorise
def standup_active(client_id, channel_id):
	"""Checks whether or not theres an active standup

	For a given channel, return whether a standup is active in it, and what 
	time the standup finishes. If no standup is active, then time_finish returns None

	Args:
		client_id: An int used to identify a specific client
		channel_id: An int used to identify a specific channel

	Returns:
		is_active: A boolean of whether or not a standup is currently active in the channel
		time_finish: A timestamp of when the standup will finish
		None: Return None when theres no active standup
	"""

	is_active = get_channel(channel_id).standup_active()
	time_finish = get_channel(channel_id).standup_time() if is_active else None

	return {"is_active": is_active,
         "time_finish": time_finish.timestamp() if time_finish else time_finish}


@export("/standup/send", methods=["POST"])
@authorise
def standup_send(client_id, channel_id, message):
	"""Adds a message to the standup queue

	Sending a message to get buffered in the standup queue, assuming a standup is currently active

	Args:
		client_id: An int used to identify a specific client
		channel_id: An int used to identify a specific channel
		message: A str representing the message body that the user wants to send

	Raises:
		ValueError: Channel ID is not a valid channel
		ValueError: Message is more than 1000 characters
		ValueError: An active standup is not currently running in this channel
	"""
	authcheck(client_id, channel_id=channel_id)
	get_channel(channel_id).standup_send(client_id, message)

	return {}
