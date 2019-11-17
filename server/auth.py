from server.AccessError import AccessError
from server.constants import * # pylint: disable=unused-wildcard-import
from server.state import * # pylint: disable=unused-wildcard-import
from server.auth_util import * # pylint: disable=unused-wildcard-import
from objects.users_object import User
import re  # used for checking email formating
from server.upload import send_mail
from server.export import export
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' # ''
"""
	Handles all authentication related functions for emails and passwords.
"""

@export('/auth/login', methods=["POST"])
def auth_login(email, password):
	'''
	Checks email and password

	Checks entered credentials is correct.Compares the email and password taken
	with data of existing users,raises error if incorrect

	Args:
		email: Email address used to register account.
		password: A str used for authentication.
	Raises:
		ValueError: Incorrect email
		ValueError: Incorrect password
		ValueError: Email is not valid
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
	Creates an account for first time users

	Takes in the information inputted and stores it in a new user object

	Args:
		email: Used to identify account
		password : A str used for authentication
		name_first: User's first name
		name_last: User's last name
	Returns:
		A dictionary storing user id and token
	Raises:
		ValueError: Email is already used
		ValueError: Email is not valid
		ValueError: Incorrect length for name
		ValueError: Incorrect length for password
	'''

	new_user = User(name_first, name_last, email, password)
	u_id = new_user.get_id()
	set_user(u_id, new_user)
	return {"token": maketok(u_id), "u_id": u_id}


@export("/auth/passwordreset_request", methods = ["POST"])
def auth_passwordreset_request(email):
	
	# Search for matching email
	for user in user_iter():
		if user.get_email() == email:
	
			# If it matches generate pw reset code
			reset_code = make_resetPw(user.get_id)
			# Create contents of email and send			
			msg = Message("Slackr Password Reset Request", recipients=email)
			msg.body = f"Your passcode for resetting your email is {reset_code}"
			send_mail(msg)
	
	return {}

@export("/auth/passwordreset_reset", methods = ["POST"])
def auth_passwordreset_reset(reset_code, new_password):
	# Check if reset code is correct
	if check_resetPw >= 0:
		# Change the password for the user
		user = get_user(check_resetPw)
		user.set_password(new_password)

	raise ValueError("Invalid reset code")

	return {}
