from datetime import datetime, timedelta

import urllib.request
from PIL import Image
from server.AccessError import AccessError
from server.constants import *
from server.state import *
from server.auth_util import *

from objects.channels_object import Channel
from objects.users_object import User


from server.export import export
import re # used for checking email formating

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' # ''

@export("/user/profile", methods=["GET"])
@authorise
def user_profile(client_id, u_id):
	'''
	shows basic information of a user

	finds the corresponding user with u_id from user global dictionary
	and retrieves relevant info

	Args:
		client_id: user ID of requester
		u_id: user ID of user who the requester wants to know about
	Returns:
		a dictionary with email, full name, and handle of selected user
	Raises:
		ValueError: u_id is invalid
	'''
	# Check for valid user
	user = get_user(u_id)
	return {"email": user.get_email(),
			"name_first": user.get_name_first(),
			"name_last": user.get_name_last(),
			"handle_str": user.get_handle_str()}


@export("/user/profile/setname", methods=["PUT"])
@authorise
def user_profile_setname(client_id, name_first, name_last):
	'''
	changes name of requester

	calls name setters from corresponding user object

	Args:
		client_id: user ID of requester
		name_first: user inputted string for new first name
		name_last: user inputted string for new last name 
	Returns:
		empty dictionary
	Raises:
		ValueErrors: name is too long or too short

	'''
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


@export("/user/profile/setemail", methods=["PUT"])
@authorise
def user_profile_setemail(client_id, email):
	'''
	changes email of requester

	calls email setters from corresponding user object

	Args:
		client_id: user ID of requester
		email: user inputted string for new email
	Returns:
		empty dictionary
	Raises:
		ValueErrors: invalid or already in use email
	'''
	# Check if email is in correct format

	if re.search(regex, email):

		# Check for email address duplicates
		for user_obj in user_iter():
				# Do not raise error if user does not change field
				if user_obj.get_id() != client_id and user_obj.get_email() == email:
					raise ValueError("Email already in use")

		get_user(client_id).set_email(email)

	else:
		raise ValueError("Invalid Email Address")

	return {}


@export("/user/profile/sethandle", methods=["PUT"])
@authorise
def user_profile_sethandle(client_id, handle_str):
	'''
	changes handle of requester

	calls handle setters from corresponding user object

	Args:
		client_id: user ID of requester
		handle_str: user inputted string for new handle
	Returns:
		empty dictionary
	Raises:
		ValueErrors: handle is too long or too short, handle is already in use
	'''
	# Check if handle str is the right len
	if len(handle_str) > 20:
		raise ValueError("Handle name is too long")
	if len(handle_str) < 3:
		raise ValueError("Handle name is too short")
	# Check if handle str is already in use by another user

	for user_obj in user_iter():
		# Do not raise error if user keeps their own name unchanged
		if user_obj.get_id() != client_id and user_obj.get_handle_str() == handle_str:
				raise ValueError("Handle name already in use")
	get_user(client_id).set_handle_str(handle_str)

	return {}


@export("/user/profiles/uploadphoto", methods=["POST"])
@authorise
def user_profiles_uploadphoto(client_id, img_url, x_start, y_start, x_end, y_end):
	# Download the image
	urllib.request.urlretrieve(img_url, "./static/" + client_id + ".pn")
	# Crop if image is too big
	if y_end > 500 or x_end > 500:
		imageObject = Image.open("./static/" + client_id + ".pn")
		cropped = imageObject.crop((0, 0, 500, 500))
		cropped.save("./static/" + client_id + ".pn")
	return {}


@export("/admin/userpermission/change", methods = ["POST"])
@authorise
def admin_userpermission_change(client_id, u_id, permission_id):
	authcheck(client_id, is_admin = True)
	if permission_id not in (OWNER, ADMIN, MEMBER):
		raise ValueError("Permission ID not valid")
	get_user(u_id).set_permission(permission_id)
	return {}