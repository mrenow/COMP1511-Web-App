from server.state import *
from server.constants import *
import re  # used for checking email formating
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  # ''

"""
	User class

    User structure containing all attributes of a user and 
    all the methods in which it can be interacted with.

    Attributes:
        _u_id: An int used to identify a specifc user
        _password: A str used for authentication
        _name_first: User's first name
        _name_last: User's last name
        _email: User's Email used to register an account
        _handle: User's Username, by default is set to user's first name + last name
        _profile_picture: An image user can set to represent them
        _channel_ids: A set of channels a user is a member of
        _owner_channel_ids: A set of channels a user owns
        _permission_id: An int indicating user permission level
"""

class User:

	def __init__(self, name_first, name_last, email, password):
		self._u_id = num_users()
		self.valid_password(password)
		self._password = password
		self.valid_first_name(name_first)
		self._name_first = name_first
		self.valid_last_name(name_last)
		self._name_last = name_last
		self.email_unused(email, None)
		self.valid_email(email)
		self._email = email
		self._handle_str = name_first + name_last
		self._profile_picture = None
		self._channel_ids = set()
		self._owner_channel_ids = set()
		if self._u_id == 0:
			self._permission_id = OWNER
		else:
			self._permission_id = MEMBER
		set_user(self._u_id, self)
		inc_users()

	def get_id(self):
		return self._u_id

	def get_name_first(self):
		return self._name_first

	def set_name_first(self, name_first):
		self.valid_first_name(name_first)
		self._name_first = name_first

	def get_name_last(self):
		return self._name_last

	def set_name_last(self, name_last):
		self.valid_last_name(name_last)
		self._name_last = name_last

	def get_email(self):
		return self._email

	def set_email(self, email, client_id):
		self.valid_email(email)
		self.email_unused(email, client_id)
		self._email = email

	def get_password(self):
		return self._password	
	
	def set_password(self, password):
		self.valid_password(password)
		self._password = password
	
	def get_permission(self):
		return self._permission_id

	def set_permission(self, permission):
		self._permission_id = permission

	def get_channels(self):
		return self._channel_ids

	def get_owner_channels(self):
		return self._owner_channel_ids

	def add_channel(self, channel_id):
		self._channel_ids.add(channel_id)

	def add_owner_channel(self,  channel_id):
		self._owner_channel_ids.add(channel_id)

	def remove_channel(self, channel_id):
		self._channel_ids.discard(channel_id)

	def remove_owner_channel(self,  channel_id):
		self._owner_channel_ids.discard(channel_id)

	def get_handle_str(self):
		return self._handle_str

	def set_handle_str(self, handle_str, client_id):
		self.handle_unused(handle_str, client_id)
		self.valid_handle(handle_str)
		self._handle_str = handle_str

	def get_user_profile(self):
		return {"email": self._email,
                    "name_first": self._name_first,
                    "name_last": self._name_last,
                    "handle_str": self._handle_str}

	def to_json(self):
		return {"u_id": self._u_id,
                    "name_first": self._name_first,
                    "name_last": self._name_last}
	
	# Check if password is too short
	def valid_password(self, password):
		'''
		Checks if password is longer than 6 characters
		
		
		Args:
			password: A str used for authentication
		Raises:
			ValueError: password too short
		'''
		if len(password) < 6:
			raise ValueError("Password too short")

	# Check if name has correct length
	def valid_first_name(self, name_first):
		'''
		Checks if name is less than 50 and greater than 1 characters
		
		
		Args:
			name_first: User's first name
		Raises:
			ValueError: name is too long
			ValueError: name is too short
		'''
		# First name within 1 and 50 characters
		if len(name_first) > 50:
			raise ValueError("First name is too long")
		if len(name_first) < 1:
			raise ValueError("First name is too short")

	# Check if name has correct length
	def valid_last_name(self, name_last):
		'''
		Checks if name is less than 50 and greater than 1 characters
		
		
		Args:
			name_last: User's last name
		Raises:
			ValueError: name is too long
			ValueError: name is too short
		'''
		if len(name_last) > 50:
			raise ValueError("Last name is too long")	
		if len(name_last) < 1:
			raise ValueError("Last name is too short")

	# Check if handle str is the right len
	def valid_handle(self, handle_str):	
		'''
		Checks if handel is less than 20 and greater than 3 characters
		
		
		Args:
			handle_str: User's handle
		Raises:
			ValueError: name is too long
			ValueError: name is too short
		'''
		if len(handle_str) > 20:
			raise ValueError("Handle name is too long")
		if len(handle_str) < 3:
			raise ValueError("Handle name is too short")

	# Checks if email is already in use
	def email_unused(self,email, client_id):
		'''
		checks email against all existing emails
		
		
		Args:
			email: Email address used to register account
			client_id: ID represneting a user
		Raises:
			ValueError: Email already in use
		'''
		for user_obj in user_iter():
				# Do not raise error if user does not change field
				if user_obj.get_id() != client_id and user_obj.get_email() == email:
					raise ValueError("Email already in use")
	# Check if email is good
	def valid_email(self,email):
		'''
		Uses re.search to check if email has correct format
		
		
		Args:
			email: Email address used to register account
		Raises:
			ValueError: Email given is invalid
		'''
		if not re.search(regex,email):
			raise ValueError("Invalid Email Address")

	# Check if handle str is already in use by another user
	def handle_unused(self, handle, client_id):
		'''
		Checks handle against all existing handles
		
		
		Args:
			handle: handle_str: User's handle
			client_id: ID represneting a user
		Raises:
			ValueError: Handle already in use
		'''
		for user_obj in user_iter():
			# Do not raise error if user keeps their own name unchanged
			if user_obj.get_id() != client_id and user_obj.get_handle_str() == handle:
				raise ValueError("Handle name already in use")
