import sys
from json import dumps
from flask import Flask, request
from datetime import datetime, timedelta
import pytz
from typing import List, Dict
from server.AccessError import AccessError
from server.constants import *
from server.state import *
from objects.channels_object import Channel
from objects.messages import Message
from objects.users_object import User

import re # used for checking email formating
import urllib.request
from PIL import Image
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' # ''
import jwt

# Initially define export to do nothing
def export(route, methods):
	def decorator(function):	
		return function
	return decorator
	
# Overwrite export with the definition given in the program's entry point if applicable
try:
	from __main__ import export
except(ImportError):
	pass

# 
# CONSTANTS 
#



tokcount = 0
valid_toks = set()


# Contains all checks to be done regularly
def update():
	
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

'''
Raises an Access error if all of the conditions specified are not met.
Usage:
Only allow if is ( owner of channel or admin or particular user ) and in channel:
>>> authcheck(u_id, user = particular_u_id, chowner = channel_id,  admin = True)
>>> authcheck(u_id, user = channel_id) 
'''


def authcheck(client_id, user_id=None, channel_id=None, chowner_id=None, is_admin=False):

	auth = False

	if user_id != None and user_id == client_id:
		auth = True
	if channel_id != None and client_id in get_channel(channel_id).get_members():
		auth = True
	if chowner_id != None and client_id in get_channel(chowner_id).get_owners():
		auth = True
	if is_admin and get_user(client_id).get_permission() in (OWNER, ADMIN):
		auth = True
	if auth:
		return

	if user_id != None:
		raise AccessError(f"auth: User {client_id} is not user {user_id}.")
	if channel_id != None:
		raise AccessError(f"auth: User {client_id} is not in channel {channel_id}")
	if chowner_id != None:
		raise AccessError(f"auth: User {client_id} is not an owner of {channel_id}.")
	if is_admin:
		raise AccessError(f"auth: User {client_id} is not admin")


def tokcheck(token) -> int:	
	
	
	payload = jwt.decode(token, private_key, algorithms= ["HS256"])
	if payload["tok_id"] in valid_toks:
		return payload["u_id"]
	raise ValueError("Invalid Token")

def maketok(u_id) -> str:
	global tokcount
	payload = {"u_id": u_id, "tok_id": tokcount, "time" : str(datetime.now(TIMEZONE))}
	valid_toks.add(tokcount)
	tokcount += 1
	return jwt.encode(payload, private_key, algorithm= "HS256")

def killtok(token) -> Dict["is_success", bool]:
	
	payload = jwt.decode(token, private_key, algorithms= ["HS256"])
	tok_id = payload["tok_id"]
	if payload["tok_id"] in valid_toks:
		valid_toks.remove(payload["tok_id"])
		return dict(is_success = True)
	return dict(is_success = False)

@export('/auth/login', methods = ["POST"])
def auth_login(email, password):
	
	#Check in users if email exists then try to match the pw
	for user in user_iter():
		if user._email == email:
				if user._password == password:		
					return dict(token = maketok(user._u_id), u_id = user._u_id)
				raise ValueError("Wrong Password for Given Email Address")
	raise ValueError("Incorrect Email Login")


@export("/auth/logout", methods = ["POST"])
def auth_logout(token):
	return killtok(token)

@export("/auth/register", methods = ["POST"])
def auth_register(email, password, name_first, name_last):

	# Check if email is good
	print(email, password)
	if not re.search(regex,email):
		raise ValueError("Invalid Email Address")
	else:

		for user in user_iter():
			if user.get_email() == email:
				raise ValueError("Email already in use")

		# Password
		if len(password) < 6:
			raise ValueError("Password too shorSt")

		# First and last name within 1 and 50 characters
		if len(name_first) > 50:
			raise ValueError("First name is too long")
		if len(name_last) > 50:
			raise ValueError("Last name is too long")
		if len(name_first) < 1:
			raise ValueError("First name is too short")
		if len(name_last) < 1:
			raise ValueError("Last name is too short")

		obj = User(name_first, name_last, email, password)
		u_id = obj.get_id()
		set_user(u_id,obj)
		return dict(token = maketok(u_id), u_id = u_id)
		
@export("/auth/passwordreset_request", methods = ["POST"])
def auth_passwordreset_request(email):
	return {}


@export("/auth/passwordreset_reset", methods = ["POST"])
def auth_passwordreset_reset(reset_code, new_password):
	return {}

@export("/channel/invite", methods = ["POST"])
def channel_invite(token, channel_id, u_id):
	client_id = tokcheck(token) 
	authcheck(client_id, channel_id = channel_id)
	get_channel(channel_id).join(u_id)

	return {}


'''
Raises a value error when channel id does not exist

'''

@export("/channel/details", methods = ["GET"])
def channel_details(token, channel_id):
	client_id = tokcheck(token)
	authcheck(client_id, channel_id = channel_id)
	return get_channel(channel_id).to_json_members()

@export("/channel/messages", methods = ["GET"])
def channel_messages(token, channel_id, start):
	client_id = tokcheck(token)	
	update()
	
	authcheck(client_id, channel_id = channel_id)
	if start > get_channel(channel_id).get_num_messages():
		raise ValueError(f"channel_messages: Start index {start} out of bounds on request to channel {channel_id}")

	end = start + 50
	message_list = get_channel(channel_id).get_message_list()
	if -start-1 < -len(message_list) or -start-51 < -len(message_list):
		end = -1
	return dict(messages = get_channel(channel_id).channel_messages(start, client_id),
				start =  start,
				end = end)

@export("/channel/leave", methods = ["POST"])
def channel_leave(token, channel_id):
	client_id = tokcheck(token)
	get_channel(channel_id).leave(client_id)
	return {}

@export("/channel/join", methods = ["POST"])
def channel_join(token, channel_id):
	client_id = tokcheck(token)
	if get_channel(channel_id).get_is_public() == False:
		raise AccessError("channel is private")
	get_channel(channel_id).join(client_id)
	return {}

@export("/channel/addowner", methods = ["POST"])
def channel_addowner(token, channel_id, u_id):
	client_id = tokcheck(token)
	authcheck (client_id, chowner_id = channel_id, is_admin = True)
	get_channel(channel_id).add_owner(u_id)

	return {}

@export("/channel/removeowner", methods = ["POST"])
def channel_removeowner(token, channel_id, u_id):
	client_id = tokcheck(token)
	authcheck (client_id, chowner_id = channel_id, is_admin = True)
	get_channel(channel_id).remove_owner(u_id)
	return {}

@export("/channels/list", methods = ["GET"])
def channels_list(token):
	client_id = tokcheck(token)
	channels_list = [get_channel(channel_id).to_json_id() for channel_id in get_user(client_id).get_channels()]
	return dict(channels = channels_list)
	
@export("/channels/listall", methods = ["GET"])
def channels_listall(token):
	"""
	Lists all channels with format 
	"""
	client_id = tokcheck(token)
	channels_list = [channel_obj.to_json_id() for channel_obj in channel_iter()]
	return dict(channels = channels_list)
	

@export("/channels/create", methods=["POST"])
def channels_create(token, name, is_public):
	
	client_id = tokcheck(token)
	authcheck(client_id, is_admin=True)

	new_channel = Channel(name, client_id, is_public)
	get_user(client_id).get_channels().add(new_channel.get_id())
	set_channel(new_channel.get_id(), new_channel)

	return dict(channel_id = new_channel.get_id())
'''
Added to the specification.
'''

@export("/channels/delete", methods = ["POST"])
def channels_delete(token, channel_id):
	client_id = tokcheck(token)
	authcheck(client_id, channel_id = channel_id)
	
	return {}


'''
if message > 1000 chars val error
'''
@export("/message/sendlater", methods = ["POST"])
def message_sendlater(token, channel_id, message, time_sent):
	
	
	if time_sent < datetime.now(TIMEZONE):
		raise ValueError(f"message_sendlater: time is {datetime.now(TIMEZONE) - time_sent} in the past")
	client_id = tokcheck(token)
	authcheck(client_id, channel_id = channel_id)
	
	message_obj = Message(message, channel_id, client_id, time_sent)
	print(get_unsent())
	return {}


'''
Ezra: done
'''
@export("/message/send", methods = ["POST"])
def message_send(token, channel_id, message):
	
	

	client_id = tokcheck(token)
	authcheck(client_id, channel_id = channel_id)
	
	message_obj = Message(message, channel_id, client_id)

	return {}

'''
Ezra: done 
'''
@export("/message/remove", methods = ["DELETE"])
def message_remove(token, message_id):

	client_id = tokcheck(token)
	mess = get_message(message_id)
	print("	",get_message(message_id).get_message())
	authcheck(client_id, channel_id = mess.get_channel())
	authcheck(client_id, user_id = mess.get_user(), chowner_id = mess.get_channel(), is_admin = True)
	mess.remove()
	return {}

'''
Ezra: done 
'''
@export("/message/edit", methods = ["PUT"])
def message_edit(token, message_id, message):
	message = message.strip()
	if not message:
		message_remove(token, message_id)
		return {}
	client_id = tokcheck(token)
	mess = get_message(message_id) 
	authcheck(client_id, channel_id = mess.get_channel())
	print("owners:",get_channel(mess.get_channel()).get_owners())
	authcheck(client_id, user_id = mess.get_user(), chowner_id = mess.get_channel(), is_admin = True)
	
	mess.set_message(message)
	return {}

'''
Ezra: done 
'''
@export("/message/react", methods = ["POST"])
def message_react(token, message_id, react_id): 
	client_id = tokcheck(token)
	mess = get_message(message_id)
	authcheck(client_id, channel_id = mess.get_channel())
	### Iteration 2 only 
	if react_id != 1:
		raise ValueError(f"message_react: React id {react_id} is not valid on message {mess.get_id}: '{mess.get_message()[:10]}...'")
	###

	if mess.has_react(react_id) and client_id in mess.get_react(react_id).get_users():
		raise ValueError(f"message_react: User {client_id} already has react_id {react_id} on message {mess.get_id()}: '{mess.get_message()[:10]}...'")
	mess.add_react(client_id, react_id)
	
	return {}

'''
Ezra: done 
'''
@export("/message/unreact", methods = ["POST"])
def message_unreact(token, message_id, react_id):
	client_id = tokcheck(token)
	mess = get_message(message_id)
	authcheck(client_id, channel_id = mess.get_channel())

	if not mess.has_react(react_id):
		raise ValueError(f"message_unreact: React_id {react_id} not on message {mess.get_id()}: '{mess.get_message()[:10]}...'")
		
	if client_id not in mess.get_react(react_id).get_users():
		raise ValueError(f"message_unreact: User {client_id} does not have react_id {react_id} on message {mess.get_id()}: '{mess.get_message()[:10]}...'")
	
	mess.remove_react(client_id, react_id)
	
	return {}

'''
Ezra: done 
'''
@export("/message/pin", methods = ["POST"])
def message_pin(token, message_id):		
	client_id = tokcheck(token)
	mess = get_message(message_id)
	if mess.is_pinned():
		raise ValueError(f"message_pin: Message {mess.get_id()} '{mess.get_message()[:10]}...' is already pinned.")
  
	authcheck(client_id, chowner_id = mess.get_channel(), is_admin = True)
	
	mess.set_pin(True)
	
	return {}

'''
Unpins message.
Value Error:

Access Error:

returns
'''
@export("/message/unpin", methods = ["POST"])
def message_unpin(token, message_id):	
	client_id = tokcheck(token)
	mess = get_message(message_id)
	
	if not mess.is_pinned():
		raise ValueError(f"message_unpin: Message {mess.get_id()} '{mess.get_message()[:10]}...' is not pinned.")
	authcheck(client_id, chowner_id = mess.get_channel(), is_admin = True)
	mess.set_pin(False)
	
	return {}

@export("/user/profile", methods = ["GET"])
def user_profile(token, u_id):
	# Check for authorisation
	client_id = tokcheck(token)
	authcheck(client_id)
	# Check for valid user
	user = get_user(u_id)
	return dict(
		email = user.get_email(),
		name_first = user.get_name_first(),
		name_last = user.get_name_last(),
		handle_str = user.get_handle_str())

  
@export("/user/profile/setname", methods = ["PUT"])
def user_profile_setname(token, name_first, name_last):
	# Check for authorisation
	client_id = tokcheck(token)
	authcheck(client_id)
	# Check if first and last names are within length restrictions otherwise return a ValueError
	if len(name_first) > 50: 
		raise ValueError("First name provided is too long")
	if len(name_last) > 50: 
		raise ValueError("Last name provided is too long")
	if len(name_first) < 1: 
		raise ValueError("First name provided is too short")
	if len(name_last) < 1: 
		raise ValueError("Last name provided is too short")
	
	get_user(client_id).set_name_first(name_first)
	get_user(client_id).set_name_last(name_last)
	
	return {}

@export("/user/profile/setemail", methods = ["PUT"])
def user_profile_setemail(token, email):
	# Check for authorisation
	client_id = tokcheck(token)
	authcheck(client_id)
	# Check if email is in correct format
	
	if(re.search(regex,email)):  
		
		# Check for email address duplicates
		for user in user_iter():
				# Do not raise error if user does not change field
				if user.get_id() != client_id and user._email == email:
					raise ValueError("Email already in use")

		get_user(client_id).set_email(email)
	
	else:  
		raise ValueError("Invalid Email Address")

	return {}

@export("/user/profile/sethandle", methods = ["PUT"])
def user_profile_sethandle(token, handle_str):
	# Check for authorisation
	client_id = tokcheck(token)
	authcheck(client_id)
	# Check if handle str is the right len
	if len(handle_str) > 20:
		raise ValueError("Handle name is too long")  
	if len(handle_str) < 3:
		raise ValueError("Handle name is too short")
	# Check if handle str is already in use by another user
	
	for user in user_iter():
		# Do not raise error if user keeps their own name unchanged
		if user.get_id() != client_id and user._handle_str == handle_str:

				raise ValueError("Handle name already in use")
	get_user(client_id).set_handle_str(handle_str)
	

	return {}

@export("/user/profiles/uploadphoto", methods = ["POST"])
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
	# Check for authorisation
	client_id = tokcheck(token)
	# Download the image
	urllib.request.urlretrieve(img_url, "./static/" + client_id + ".pn")
	# Crop if image is too big 
	if y_end > 500 or x_end > 500:
		imageObject = Image.open("./static/" + client_id + ".pn")
		cropped = imageObject.crop((0,0,500,500))
		cropped.save("./static/" + client_id + ".pn")
		
	return {}

@export("/standup/start", methods = ["POST"])
def standup_start(token, channel_id, length):
	
	client_id = tokcheck(token)
	authcheck(client_id, channel_id = channel_id)

	# Raises an error if standup already active
	time_finish = get_channel(channel_id).standup_start(client_id, length)


	return dict(time_finish = time_finish)

@export("/standup/send", methods = ["POST"])
def standup_send(token, channel_id, message):
	
	client_id = tokcheck(token)
	authcheck(client_id, channel_id = channel_id)
	get_channel(channel_id).standup_send(client_id, message)

	return {}
@export("/standup/active", methods = ["GET"])
def standup_active(token, channel_id):
	
	client_id = tokcheck(token)
	
	is_active = get_channel(channel_id).standup_active()
	time_finish = get_channel(channel_id).standup_time() if is_active else None
	
	return dict(is_active = is_active,
					time_finish = time_finish.timestamp() if time_finish else time_finish)


@export("/search", methods = ["GET"])
def search(token, query_str):
	return {}
	
@export("/admin/userpermission/change", methods = ["POST"])
def admin_userpermission_change(token, u_id, permission_id):
	user_id = tokcheck(token)
	authcheck(user_id, is_admin = True)
	if permission_id not in (OWNER, ADMIN, MEMBER):
		raise ValueError("Permission ID not valid")
	get_user(u_id).set_permission(permission_id)
	return {}

def relevance_score(string):
	return 1
	
def sort_message(msg_list):
	msg_list.sort(key = relevance_score)
	return msg_list
