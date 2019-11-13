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

	print("to send", get_unsent())
	lock_unsent()
	try:
		for index, m in enumerate(get_unsent()):
			print(m.get_time(), datetime.now(TIMEZONE))
			if m.get_time() < datetime.now(TIMEZONE):
				get_channel(m.get_channel()).send_message(m.get_id())
				del get_unsent()[index]
	# Always release lock please thankyou
	finally:
		release_unsent()


@export("/channel/invite", methods=["POST"])
@authorise
def channel_invite(client_id, channel_id, u_id):
	authcheck(client_id, channel_id=channel_id)
	get_channel(channel_id).join(u_id)
	return {}


'''
Raises a value error when channel id does not exist

'''


@export("/channel/details", methods=["GET"])
@authorise
def channel_details(client_id, channel_id):
	authcheck(client_id, channel_id=channel_id)
	return get_channel(channel_id).to_json_members()


@export("/channel/messages", methods=["GET"])
@authorise
def channel_messages(client_id, channel_id, start):
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
	get_channel(channel_id).leave(client_id)
	return {}


@export("/channel/join", methods=["POST"])
@authorise
def channel_join(client_id, channel_id):
	if get_channel(channel_id).get_is_public() == False:
		raise AccessError("Channel is private")
	get_channel(channel_id).join(client_id)
	return {}


@export("/channel/addowner", methods=["POST"])
@authorise
def channel_addowner(client_id, channel_id, u_id):
	authcheck(client_id, chowner_id=channel_id, is_admin=True)
	get_channel(channel_id).add_owner(u_id)

	return {}


@export("/channel/removeowner", methods=["POST"])
@authorise
def channel_removeowner(client_id, channel_id, u_id):
	authcheck(client_id, chowner_id=channel_id, is_admin=True)
	get_channel(channel_id).remove_owner(u_id)
	return {}


@export("/channels/list", methods=["GET"])
@authorise
def channels_list(client_id):
	channels_list = [get_channel(channel_id).to_json_id()
                  for channel_id in get_user(client_id).get_channels()]
	return {"channels": channels_list}


@export("/channels/listall", methods=["GET"])
@authorise
def channels_listall(client_id):
	channels_list = [channel_obj.to_json_id() for channel_obj in channel_iter()]
	return {"channels": channels_list}


@export("/channels/create", methods=["POST"])
@authorise
def channels_create(client_id, name, is_public):
	authcheck(client_id, is_admin=True)
	new_channel = Channel(name, client_id, is_public)
	get_user(client_id).get_channels().add(new_channel.get_id())
	set_channel(new_channel.get_id(), new_channel)

	return {"channel_id": new_channel.get_id()}
