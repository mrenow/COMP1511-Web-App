import jwt
from datetime import datetime, timedelta
from server.AccessError import AccessError
from server.constants import *
from server.state import *


tokcount = 0
valid_toks = set()


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
		raise AccessError(f"User {client_id} is not user {user_id}.")
	if channel_id != None:
		raise AccessError(f"User {client_id} is not in channel {channel_id}")
	if chowner_id != None:
		raise AccessError(f"User {client_id} is not an owner of {channel_id}.")
	if is_admin:
		raise AccessError(f"User {client_id} is not admin")


def authorise(function):
	'''
	Turns func(token, **kwargs) into func(client_id, **kwargs), throwing a value
	error if token is not 

	checks a token is in valid_toks and then returns the u_id within the payload

	Args:
		token: a encoded string used for getting user ID for authorization
	Returns: 
		a user id contained encrypted in the token
	Raises:
		ValueError: token is invalid

	'''
	def wrapper(token, *args, **kwargs):

		try:
			payload = jwt.decode(token, private_key, algorithms=["HS256"])
		except(Exception):
			return ValueError("Invalid Token")

		if payload["tok_id"] not in valid_toks:
			raise ValueError("Invalid Token")

		client_id = payload["u_id"]

		return function(client_id, *args, **kwargs)
	wrapper.__name__ = function.__name__
	return wrapper


def maketok(u_id):
	'''
	Creates a token for a user.

	Generates a token with u_id that is encrypted in its payload

	Args: 
		u_id:a number representing used to identify a user
	Returns:
		A token with a payload that is encrypted

	'''
	global tokcount
	payload = {"u_id": u_id, "tok_id": tokcount,
            "time": str(datetime.now(TIMEZONE))}
	valid_toks.add(tokcount)
	tokcount += 1
	return jwt.encode(payload, private_key, algorithm="HS256")


def killtok(token):
	'''
	removes specific token 

	looks through a list of valid tokens and removes given token

	Args:
		token: a encoded string used for getting user ID for authorization
	Returns: 
		returns a dictionary indicating whether decoding was successful
	'''
	payload = jwt.decode(token, private_key, algorithms=["HS256"])
	tok_id = payload["tok_id"]
	
	if payload["tok_id"] in valid_toks:
		valid_toks.remove(tok_id)
		return {"is_success": True}
	return {"is_success": False}
