from datetime import datetime, timedelta
from server.AccessError import AccessError
from server.constants import *
from server.state import *
from server.auth_util import *
from objects.channels_object import Channel
from objects.messages import Message
from objects.users_object import User

from server.export import export

# Contains all checks to be done regularly


def update_messages():
	"""
	Updates the server's message state. Sends all messages that are due to be sent.
	"""
	lock_unsent()
	try:
		# Sends all messages which have a time greater than the current time.
		for index, message_obj in enumerate(get_unsent()):
			if message_obj.get_time() < datetime.now(TIMEZONE):
				get_channel(message_obj.get_channel()).send_message(message_obj.get_id())
				del get_unsent()[index]
	# Always release lock please thankyou
	finally:
		release_unsent()


@export("/channel/invite", methods=["POST"])
@authorise
def channel_invite(client_id, channel_id, u_id):
	"""
	Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited
	the user is added to the channel immediately.
	
	Args:
		client_id: ID of requester.
		channel_id: ID of the channel.
		u_id: ID of the user.
	Returns:
		Empty dictionary.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
		AccessError: Requester is not a member of the specified channel.
	"""
	authcheck(client_id, channel_id=channel_id)
	get_channel(channel_id).join(u_id)
	return {}


@export("/channel/details", methods=["GET"])
@authorise
def channel_details(client_id, channel_id):
	"""
	Given a Channel with ID channel_id that the authorised user is part of, provide
	basic details about the channel.

	Args:
		client_id: ID of requester.
		channel_id: ID of the channel.
	Returns:
		A dictionary of {name, owner_members, all_members}
			name: String denoting the name of the channel.
			owner_members: List of jsons representing each owner.
			all_members: List of jsons representing each member.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
		AccessError: Requester is not a member of the specified channel.
	"""
	authcheck(client_id, channel_id=channel_id)
	return get_channel(channel_id).to_members_json()


@export("/channel/messages", methods=["GET"])
@authorise
def channel_messages(client_id, channel_id, start):
	"""
	Given a Channel with ID channel_id that the authorised user is part of, return up to
	50 messages between index "start" and "start + 50". Message with index 0 is the most
	recent message in the channel. This function returns a new index "end" which is the
	value of "start + 50", or, if this function has returned the least recent messages
	in the channel, returns -1 in "end" to indicate there are no more messages to
	load after this return.
	
	Args:
		client_id: ID of requester.
		channel_id: ID of the channel.
		start: Starting index to return messages from.
	Returns:
		A dictionary of {messages, start, end}
			messages: An ordered list of messages jsons from earliest to latest. 
			start: Starting index to messages were returned from.
			end: Index following the last message returned, or -1 when last message was
				the last message in the channel.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
		ValueError: Start index is out of bounds.
		AccessError: Requester is not a member of the specified channel.
	"""
	# Update before sending data.
	update_messages()

	authcheck(client_id, channel_id=channel_id)
	if start > get_channel(channel_id).get_num_messages():
		raise ValueError(
			f"channel_messages: Start index {start} out of bounds on request to channel {channel_id}")

	end = start + 50
	message_list = get_channel(channel_id).get_message_list()
	if -start-1 < -len(message_list) or -start-51 < -len(message_list):
		end = -1
	return {"messages": get_channel(channel_id).channel_messages(start, client_id),
         "start": start,
         "end": end}


@export("/channel/leave", methods=["POST"])
@authorise
def channel_leave(client_id, channel_id):
	"""
	Given a channel ID, the user removed as a member of this channel
	
	Args:
		client_id: ID of requester.
		channel_id: ID of the channel.
	Returns:
		Empty dictionary.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
		AccessError: Requester is not a member of channel with channel_id
	"""
	get_channel(channel_id).leave(client_id)
	return {}


@export("/channel/join", methods=["POST"])
@authorise
def channel_join(client_id, channel_id):
	"""
	Given a channel_id of a channel that the authorised user can join, adds them to that channel.
	
	Args:
		client_id: ID of requester.
		channel_id: ID of the channel.
	Returns:
		Empty dictionary.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
		AccessError: When none of the following are true:
			- Channel is public.
			- Requester is an owner of the server.
	"""
	if get_channel(channel_id).get_is_public() == False:
		raise AccessError("Channel is private")
	get_channel(channel_id).join(client_id)
	return {}


@export("/channel/addowner", methods=["POST"])
@authorise
def channel_addowner(client_id, channel_id, u_id):
	"""
	Make user with user id u_id an owner of this channe
	
	Args:
		client_id: ID of requester.
		channel_id: ID of the channel.
		u_id: ID of the new owner.
	Returns:
		Empty dictionary.
	Raies:
		ValueError: Any one of the input IDs do not exist on this server.
		ValuerError: Target user is already an owner of this channel.
		AccessError: When none of the following are true:
			- Requester is an owner of this channel.
			- Requester is an owner of the server.
	"""
	authcheck(client_id, chowner_id=channel_id, is_admin=True)
	get_channel(channel_id).add_owner(u_id)

	return {}


@export("/channel/removeowner", methods=["POST"])
@authorise
def channel_removeowner(client_id, channel_id, u_id):
	"""
	Remove user with user id u_id an owner of this channel

	Args:
		client_id: ID of requester.
		channel_id: ID of the channel.
		u_id: ID of the new owner.
	Returns:
		Empty dictionary.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
		ValueError: Target user is not an owner of this channel.
		AccessError: When none of the following are true:
			- Requester is an owner of this channel.
			- Requester is an owner of the server.
	"""
	authcheck(client_id, chowner_id=channel_id, is_admin=True)
	get_channel(channel_id).remove_owner(u_id)
	return {}


@export("/channels/list", methods=["GET"])
@authorise
def channels_list(client_id):
	"""
	Provide a list of all channels (and their associated details) that the authorised 
	user is part of.
	Args:
		client_id: ID of the requester.
	Returns:
		List of channel jsons with the name and ID of all channels on the server the user
		is a member of.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
	"""
	channels_list = [get_channel(channel_id).to_id_json()
                  for channel_id in get_user(client_id).get_channels()]
	return {"channels": channels_list}


@export("/channels/listall", methods=["GET"])
@authorise
def channels_listall(client_id):
	"""
	Provide a list of all channels (and their associated details) that the authorised
	user is part of.
	Args:
		client_id: ID of the requester.
	Returns:
		List of channel jsons with the name and ID of all channels on this server.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
	"""
	channels_list = [channel_obj.to_id_json() for channel_obj in channel_iter()]
	return {"channels": channels_list}


@export("/channels/create", methods=["POST"])
@authorise
def channels_create(client_id, name, is_public):
	"""
	Creates a new channel with that name that is either a public or private channel
	Args:
		client_id: ID of the requester.
		name: String identifying the channel on frontend.
		is_public: A boolean denoting whether the channel permits unrestricted joining.
	Returns:
		Dictionary of {channel_id}:
			channel_id:	ID of the newly created channel.
	Raises:
		ValueError: Any one of the input IDs do not exist on this server.
	"""
	authcheck(client_id, is_admin=True)
	# Create new channel and add the creator as a member.
	new_channel = Channel(name, client_id, is_public)
	
	return {"channel_id": new_channel.get_id()}
