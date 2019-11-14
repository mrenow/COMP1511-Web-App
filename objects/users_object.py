from server.state import *
from server.constants import *
import re  # used for checking email formating
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  # ''

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
		self.valid_email(regex, email)
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
		self.valid_email(regex, email)
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

	def valid_password(self, password):
		if len(password) < 6:
			raise ValueError("Password too short")

	def valid_first_name(self, name_first):
		# First name within 1 and 50 characters
		if len(name_first) > 50:
			raise ValueError("First name is too long")
		if len(name_first) < 1:
			raise ValueError("First name is too short")

	def valid_last_name(self, name_last):
		if len(name_last) > 50:
			raise ValueError("Last name is too long")	
		if len(name_last) < 1:
			raise ValueError("Last name is too short")

	def valid_handle(self, handle_str):
			# Check if handle str is the right len
		if len(handle_str) > 20:
			raise ValueError("Handle name is too long")
		if len(handle_str) < 3:
			raise ValueError("Handle name is too short")

	# Checks if email is already in use
	def email_unused(self,email, client_id):
		for user_obj in user_iter():
				# Do not raise error if user does not change field
				if user_obj.get_id() != client_id and user_obj.get_email() == email:
					raise ValueError("Email already in use")
	# Check if email is good
	def valid_email(self,regex,email):
		if not re.search(regex, email):
			raise ValueError("Invalid Email Address")

	# Check if handle str is already in use by another user
	def handle_unused(self, handle, client_id):
		for user_obj in user_iter():
		# Do not raise error if user keeps their own name unchanged
			if user_obj.get_id() != client_id and user_obj.get_handle_str() == handle:
				raise ValueError("Handle name already in use")