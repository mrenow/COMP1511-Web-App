from datetime import datetime, timedelta
from server.AccessError import AccessError
from server.constants import *# pylint: disable=unused-wildcard-import
from server.state import *# pylint: disable=unused-wildcard-import
from server.auth_util import *# pylint: disable=unused-wildcard-import

from objects.channels_object import Channel
from objects.messages import Message

from server.export import export

@export("/message/sendlater", methods=["POST"])
@authorise
def message_sendlater(client_id, channel_id, message, time_sent):
	"""Sends a message later at a given time.
	
	Send a message from authorised_user to the channel specified by 
	channel_id automatically at a specified time in the future

	Args: 
		client_id: An int used to identify a specific client
		channel_id: An int used to identify a specific channel
		message: A str representing the message body that the user wants to send
		time_sent: A timestamp in which the user wants the send the message

	Returns:
		message_id: An int that is used to help identitfy the message sent

	Raises:
		ValueError: When sent_time is at an earlier timestamp than the current time
	"""

	# Check if desired time to send message is past already
	if time_sent < datetime.now(TIMEZONE):
		raise ValueError(
			f"message_sendlater: time is {datetime.now(TIMEZONE) - time_sent} in the past")
	# Authentication
	authcheck(client_id, channel_id=channel_id)
	
	# Create the message object
	message_obj = Message(message, channel_id, client_id, time_sent)
	### WHATS THIS ?  print(get_unsent())
	return {}


'''
Ezra: done
'''
@export("/message/send", methods=["POST"])
@authorise
def message_send(client_id, channel_id, message):
	"""Sends a message

	Send a message from authorised_user to the channel specified by channel_id

	Args: 
		client_id: An int used to identify a specific client
		channel_id: An int used to identify a specific channel
		message: A str representing the message body that the user wants to send
	
	Returns:
		message_id: An int that is used to help identitfy the message sent

	Raises:
		ValueError: When message is over 1000 characters long
		AccessError:  The authorised user has not joined the channel they are trying to post to
	"""
	# Authentication
	authcheck(client_id, channel_id=channel_id)
	# Create the message object
	message_obj = Message(message, channel_id, client_id)

	return {}


'''
Ezra: done 
'''
@export("/message/remove", methods=["DELETE"])
@authorise
def message_remove(client_id, message_id):
	"""Removes a message

	Given a message_id for a message, this message is removed from the channel
	if the person requesting this is an admin or the one who posted it

	Args: 
		client_id: An int used to identify a specific client
		message_id: An int used to identify a specific message
	
	Raises:
		AccessError: When none of these conditions are met:
			- Message with message_id was sent by the authorised user making this request
			- The authorised user is an admin or owner of this channel or the slackr
	"""
	mess = get_message(message_id)
	print("	", get_message(message_id).get_message())
	authcheck(client_id, channel_id=mess.get_channel())
	authcheck(client_id, user_id=mess.get_user(),
	          chowner_id=mess.get_channel(), is_admin=True)
	mess.remove()
	return {}


'''
Ezra: done 
'''
@export("/message/edit", methods=["PUT"])
@authorise
def message_edit(client_id, message_id, message):
	"""Edits a message

	Given a message, update it's text with new text, provided the 
	user requesting this has the authority to. If the new message 
	is an empty string, the message is deleted.

	Args: 
		client_id: An int used to identify a specific client
		message_id: An int used to identify a specific message
		message: A str representing the message body that the user wants to send

	Raises:
		AccessError: When none of these conditions are met:
			- Message with message_id was sent by the authorised user making this request
			- The authorised user is an admin or owner of this channel or the slackr
	"""

	message = message.strip()
	mess = get_message(message_id)

	authcheck(client_id, channel_id=mess.get_channel())
	authcheck(client_id, user_id=mess.get_user(),
	          chowner_id=mess.get_channel(), is_admin=True)

	if not message:
		mess.remove()
	else:
		mess.set_message(message)
	return {}


'''
Ezra: done 
'''
@export("/message/react", methods=["POST"])
@authorise
def message_react(client_id, message_id, react_id):
	"""React with a like to the message

	Given a message within a channel the authorised user is part 
	of, add a "react" to that particular message

	Args: 
		client_id: An int used to identify a specific client
		message_id: An int used to identify a specific message
		react_id: An int used to identify a specific reaction

	Raises:
		ValueError: When none of these conditions are met:
			- message_id is not a valid message within a channel that the authorised user has joined
			- react_id is not a valid React ID. The only valid react ID the frontend has is 1
			- Message with ID message_id already contains an active React with ID react_id
	"""

	mess = get_message(message_id)
	authcheck(client_id, channel_id=mess.get_channel())
	### Iteration 2 only
	if react_id != 1:
		raise ValueError(
			f"message_react: React id {react_id} is not valid on message {mess.get_id}: '{mess.get_message()[:10]}...'")
	###

	if mess.has_react(react_id) and client_id in mess.get_react(react_id).get_users():
		raise ValueError(
			f"message_react: User {client_id} already has react_id {react_id} on message {mess.get_id()}: '{mess.get_message()[:10]}...'")
	mess.add_react(client_id, react_id)

	return {}


'''
Ezra: done 
'''
@export("/message/unreact", methods=["POST"])
@authorise
def message_unreact(client_id, message_id, react_id):
	"""Unreacts a post

	Given a message within a channel the authorised user is part of, 
	remove a "react" to that particular message

	Args: 
		client_id: An int used to identify a specific client
		message_id: An int used to identify a specific message
		react_id: An int used to identify a specific reaction

	Raises:
		ValueError: When none of these conditions are met:
			- message_id is not a valid message within a channel that the authorised user has joined
			- react_id is not a valid React ID. The only valid react ID the frontend has is 1
			- Message with ID message_id already contains an active React with ID react_id
	"""

	mess = get_message(message_id)
	authcheck(client_id, channel_id=mess.get_channel())

	if not mess.has_react(react_id):
		raise ValueError(
			f"message_unreact: React_id {react_id} not on message {mess.get_id()}: '{mess.get_message()[:10]}...'")

	if client_id not in mess.get_react(react_id).get_users():
		raise ValueError(
			f"message_unreact: User {client_id} does not have react_id {react_id} on message {mess.get_id()}: '{mess.get_message()[:10]}...'")

	mess.remove_react(client_id, react_id)

	return {}


'''
Ezra: done 
'''
@export("/message/pin", methods=["POST"])
@authorise
def message_pin(client_id, message_id):
	"""Pins a message 

	Given a message within a channel, mark it as "pinned" to be 
	given special display treatment by the frontend

	Args: 
		client_id: An int used to identify a specific client
		message_id: An int used to identify a specific message
	
	Raises:
		ValueError: message_id is not a valid message
		ValueError: The authorised user is not an admin
		ValueError: Message with ID message_id is already pinned
		AccessError: The authorised user is not a member of the channel that the message is within
	"""

	mess = get_message(message_id)
	if mess.is_pinned():
		raise ValueError(
			f"message_pin: Message {mess.get_id()} '{mess.get_message()[:10]}...' is already pinned.")

	authcheck(client_id, chowner_id=mess.get_channel(), is_admin=True)

	mess.set_pin(True)

	return {}


@export("/message/unpin", methods=["POST"])
@authorise
def message_unpin(client_id, message_id):
	"""
	Upins message

	Given a message within a channel, remove it's mark as unpinned

	Args: 
		client_id: An int used to identify a specific client
		message_id: An int used to identify a specific message
	
	Raises:
		ValueError: message_id is not a valid message
		ValueError: The authorised user is not an admin
		ValueError: Message with ID message_id is already unpinned
		AccessError: The authorised user is not a member of the channel that the message is within
	"""

	mess = get_message(message_id)

	if not mess.is_pinned():
		raise ValueError(
			f"message_unpin: Message {mess.get_id()} '{mess.get_message()[:10]}...' is not pinned.")
	authcheck(client_id, chowner_id=mess.get_channel(), is_admin=True)
	mess.set_pin(False)

	return {}


@export("/search", methods=["GET"])
@authorise
def search(client_id, query_str):
	"""
	Searches for messages that match query_str

	Given a query string, return a collection of messages 
	in all of the channels that the user has joined that match the query

	Args: 
		client_id: An int used to identify a specific client
		query_str: A str representing the message body the user wants to search

	Returns:
		message[]: A list of messages that matches the given query_str
	"""

	return {}


def relevance_score(string):
	return 1


def sort_message(msg_list):
	msg_list.sort(key=relevance_score)
	return msg_list
