from server.AccessError import AccessError
from server.constants import *
from server.state import *
from server.auth_util import *
from objects.users_object import User
import re  # used for checking email formating

from server.export import export
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  # ''
"""
	
    
"""

@export('/auth/login', methods=["POST"])
def auth_login(email, password):
	'''
	checks email and password

	Checks entered credentials is correct.Compares the email and password taken 
	with data of existing users,raises error if incorrect

	Args: 
		email
		password
	Returns:
		Nothing
	Raises:
		ValueError: Incorrect email or password
	'''
	#Check in users if email exists then try to match the pw
	for user_obj in user_iter():
		if user_obj.get_email() == email:
				if user_obj.get_password() == password:
					return {"token" : maketok(user_obj.get_id()), "u_id" : user_obj.get_id()}
				raise ValueError("Wrong Password for Given Email Address")
	raise ValueError("Incorrect Email Login")


@export("/auth/logout", methods=["POST"])
def auth_logout(token):
	'''
	logs the user out of active session

	calls killtok with given token, killtok then removes token
	from valid token list

	Args:
		token: a encoded string used for getting user ID for authorization
	Returns:
		a dictionary indicating whether if log out is successful
	'''

	return killtok(token)


@export("/auth/register", methods=["POST"])
def auth_register(email, password, name_first, name_last):
	'''
	creates an account for first time users

	takes in the information inputted and stores it in a new user object

	Args:
		email: used to identify account
		password :
		name_first: user's first name
		name_last: user's last name
	Returns: 
		a dictionary storing user id and token 
	Raises:
		ValueError: invalid or existing email, incorrect length for name or passowrd
	'''
	
	new_user = User(name_first, name_last, email, password)
	u_id = new_user.get_id()
	set_user(u_id, new_user)
	return {"token": maketok(u_id), "u_id": u_id}


@export("/auth/passwordreset_request", methods=["POST"])
def auth_passwordreset_request(email):
	return {}


@export("/auth/passwordreset_reset", methods=["POST"])
def auth_passwordreset_reset(reset_code, new_password):
	return {}
