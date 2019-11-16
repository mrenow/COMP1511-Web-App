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

'''
	Handles all user profile and permission change related functions.
'''


@export("/user/profile", methods=["GET"])
@authorise
def user_profile(client_id, u_id):
	'''
	Shows basic information of a user

	Finds the corresponding user with u_id from user global dictionary
	and retrieves relevant info

	Args:
		client_id: User ID of requester
		u_id: User ID of user who the requester wants to know about
	Returns:
		A dictionary with email, full name, and handle of selected user
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
	Changes name of requester

	Calls name setters from corresponding user object

	Args:
		client_id: User ID of requester
		name_first: User inputted string for new first name
		name_last: User inputted string for new last name 
	Returns:
		Empty dictionary
	Raises:
		ValueErrors: Name is too long or too short

	'''

	get_user(client_id).set_name_first(name_first)
	get_user(client_id).set_name_last(name_last)

	return {}


@export("/user/profile/setemail", methods=["PUT"])
@authorise
def user_profile_setemail(client_id, email):
	'''
	Changes email of requester

	Calls email setters from corresponding user object

	Args:
		client_id: User ID of requester
		email: User inputted string for new email
	Returns:
		Empty dictionary
	Raises:
		ValueErrors: Invalid email address
		ValueErrors: Email address already in use 
	'''
	# Check if email is in correct format

	get_user(client_id).set_email(email, client_id)

	return {}


@export("/user/profile/sethandle", methods=["PUT"])
@authorise
def user_profile_sethandle(client_id, handle_str):
	'''
	Changes handle of requester

	Calls handle setters from corresponding user object

	Args:
		client_id: User ID of requester
		handle_str: User inputted string for new handle
	Returns:
		Empty dictionary
	Raises:
		ValueErrors: Handle is too long or too short, handle is already in use
		ValueErrors: Handle is already used by another user
	'''
	
	get_user(client_id).set_handle_str(handle_str, client_id)

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


@export("/admin/userpermission/change", methods=["POST"])
@authorise
def admin_userpermission_change(client_id, u_id, permission_id):
	'''
	Changes permission level for a user

	Calls handle setters from corresponding user object

	Args:
		client_id: User ID of requester
		u_id: user ID of change target
		permission_id: ID representing level of permission
	Returns:
		empty dictionary
	Raises:
		ValueErrors: u_id does not refer to a valid user
		ValueErrors: Permission_id does not refer to a value permission
		AccessError: The authorised user is not an admin or owner
	'''
	authcheck(client_id, is_admin=True)
	if permission_id not in (OWNER, ADMIN, MEMBER):
		raise ValueError("Permission ID not valid")
	get_user(u_id).set_permission(permission_id)
	return {}
