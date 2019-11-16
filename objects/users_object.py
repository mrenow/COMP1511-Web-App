from server.state import *
from server.constants import *


class User:

	def __init__(self, name_first, name_last, email, password):
		self._u_id = num_users()
		self._password = password
		self._name_first = name_first
		self._name_last = name_last
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
		self._name_first = name_first

	def get_name_last(self):
		return self._name_last

	def set_name_last(self, name_last):
		self._name_last = name_last

	def get_email(self):
		return self._email

	def set_email(self, email):
		self._email = email

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

	def set_handle_str(self, handle_str):
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
