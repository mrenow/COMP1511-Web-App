from datetime import datetime, timedelta
from .messages import Message
from server.state import *
from server.constants import *

class Channel:
	"""
	An object representing a channel.

	Attributes:
		_name: String that will be displayed to identify the channel in the frontend.
		_id: Channel's ID number, used as a key in the global dictionary to obtain the object.
		_is_public: Boolean denoting whether anyone can join the channel without invitation.
		_message_list: List of message ID's in order of time sent. Most recent message is at index 0.

		_owners_set: set of the IDs of all owners of the channel.
		_members_set: Set of the IDs of all members in the channel. Also includes all owners.

		_standup_message_id: ID of the message that is the current channel's latest standup. Equals None
			if no standup has ever been initiated. A standup is active if the message's is_sent() returns false.
	"""

	def __init__(self, name, owner_id, is_public):
		"""
		Sets up a channel object with name and owner which may or may not be private.

		Args:
			name: Name of channel.
			owner_id: ID of channel creator.
			is_public: Boolean denoting public status.
		Raises:
			ValueError: Owner does not exist.
		"""
		self.set_name(name)
		self._owners_set = set([owner_id])
		self._members_set = set([owner_id])
		self._is_public = is_public
		self._id = num_channels()
		inc_channels()

		# Functions as the entire standup
		self._standup_message_id = None

		# Message list contains message_id
		self._message_list = []

		set_channel(self._id, self)
		get_user(owner_id).get_channels().add(self._id)
		get_user(owner_id).get_owner_channels().add(self._id)

	def set_is_public(self, is_public):
		self._is_public = is_public

	def set_name(self,name):
		"""
		Args:
			name: New name for this user.
		Raises:
			ValueError: Name is too long
		"""
		if len(name) > 20:
			raise ValueError("Name cannot be over 20 characters")
		self._name = name
		
	def get_name(self):
		return self._name

	def get_owners(self):
		return self._owners_set

	def get_members(self):
		return self._members_set

	def get_is_public(self):
		return self._is_public

	def get_id(self):
		return self._id

	def get_message_list(self):
		return self._message_list

	def get_num_messages(self):
		return len(self._message_list)

	def send_message(self, message_id):
		"""
		Appends a message to the front of the message list and marks the message as sent.

		Args:
			message_id: ID of the message.
		Raises:
			ValueError: Message does not exist.
		"""
		self._message_list.insert(0, message_id)
		get_message(message_id).send()

	def standup_active(self):
		# Standup_message_id is None when no standup has ever been sent and standups deactivate
		# after the message has been sent.
		return self._standup_message_id != None and not get_message(self._standup_message_id).is_sent()

	def standup_start(self, u_id, duration_seconds):
		"""
		Begins a standup in this channel for a specified duration. Standup will send automatically
		at the next server request after the duration elapses.

		Args:
			u_id: ID of the user.
			duration_seconds: Length of the new standup in seconds.
		Returns:
			time_finish: Datetime of the new standup's finish time.
		Raises:
			ValueError: User does not exist.
			ValueError: Standup already active in this channel.
			ValueError: Duration is too long.
		"""
		if self.standup_active():
			raise ValueError(f"Standup already active in channel {self._name}.")
		if duration_seconds > MAX_STANDUP_SECONDS:
			raise ValueError(
				f"Standup duration ({duration_seconds}s) exceeds maximum ({MAX_STANDUP_SECONDS}s).")
		time_finish = datetime.now(TIMEZONE) + timedelta(seconds=duration_seconds)

		# Make a new standup message where the base text is the default starting message
		new_message =  Message(STANDUP_START_STR, self._id, u_id, time=time_finish, is_standup=True)

		# Latest channel standup is now the new message
		self._standup_message_id = new_message.get_id()
		return time_finish

	def standup_send(self, u_id, text):
		"""
		Appends a user's entry to the current standup.

		Args:
			u_id: Id of the sender.
			text: String which is the message's body.
		Raises:
			ValueError: This channel does not have an active standup.
			ValueError: Message is too long.
			ValueError: User does not exist.
		"""
		if not self.standup_active():
			raise ValueError(f"No standup active in channel {self._name}")
		if MAX_MESSAGE_LEN < len(text):
			raise ValueError(
				f"Message '{text[:10]}...' with length {len(text)} exceeds maximum allowable length {MAX_MESSAGE_LEN}.")

		full_text = f"\n{get_user(u_id).get_name_first()}: {text}"
		message = get_message(self._standup_message_id)

		# Append full_text to standup message.
		message.set_message(message.get_message() + full_text)

	def standup_time(self):
		'''
		Retreives the finishing time of the current standup

		Returns:
			A datetime object that represents the completion datetime of the last standup initiated on the channel.
			datetime.min is returned if no standup has ever been initiated.
		'''
		# Return earliest possible time if no standup has ever been initiated
		if self._standup_message_id == None:
			return datetime.min
		else:
			return get_message(self._standup_message_id).get_time()

	def channel_messages(self, start, u_id):
		'''
		Retrieves a page of messages from the server.


		Args:
			u_id: ID of the user.
			start: Index of first message to be returned.
		Returns:
			A list containing the next 50 messages starting from the the start index specified.
			If there are less than 50 messages left, it returns as many messages as possible.
		'''
		# Gets the last 50 messages
		return [get_message(mess).to_json(u_id) for mess in self._message_list[start: start+50]]

	def delete_message(self, message_id):
		"""
		Deletes a message from this channel's message_list, preserving order.

		Args:
			message_id: ID of the message.
		Raises:
			ValueError: Message ID does not exist in channel
		"""
		for index, entry in enumerate(self._message_list):
			if message_id == entry:
				del self._message_list[index]
				return
		ValueError(f"Message {message_id} not found")

	def join(self, u_id):
		"""
		Joins a user to this channel.

		Args:
			u_id: ID of the user.
		Raises:
			ValueError: User does not exist.
		"""
		self._members_set.add(u_id)
		get_user(u_id).get_channels().add(self._id)

	def leave(self, u_id):
		"""
		Removes a user from the channel.

		Args:
			u_id: ID of the user
		Raises:
			ValueError: User does not exist.
		"""
		self._members_set.discard(u_id)

		# Leaving a channel also removes owner status
		if u_id in self._owners_set:
			self._owners_set.discard(u_id)
		get_user(u_id).get_channels().discard(self._id)


	def to_members_json(self):
		"""
		Converts channel information to json format for displaying members.

		Returns:
			A dictionary of {name, owner_members, all_members}:
				name: String denoting the name of the channel.
				owner_members: List of jsons representing each owner.
				all_members: List of jsons representing each member.
		"""
		return dict(name=self._name,
                    owner_members=[get_user(u_id).to_json() for u_id in self._owners_set],
                    all_members=[get_user(u_id).to_json() for u_id in self._members_set])

	def to_id_json(self):
		"""
		Converts channel infomation into a format for simple listing.

		Returns:
			A dictionary of {name, channel_id}:
				name: String denoting the name of the channel.
				channel_id: ID of this channel.
		"""
		return dict(name=self._name,
                    channel_id=self._id)

	def add_owner(self, u_id):
		"""
		Promotes a user to an owner of this channel

		Args:
			u_id: ID of the user.
		Raises:
			ValueError: User does not exist.
			ValueError: User is already an owner.
		"""
		if u_id in self._owners_set:
			raise ValueError(
				f"User {u_id} is already an owner of channel {self._id}")
		# Update self and user
		self._owners_set.add(u_id)
		get_user(u_id).get_channels().add(self._id)
		# Join channel if not already a member
		self.join(u_id)

	def remove_owner(self, u_id):
		"""
		Promotes a user to an owner of this channel

		Args:
			u_id: ID of the user.
		Raises:
			ValueError: User does not exist.
			ValueError: User is not an owner.
		"""
		if u_id not in self._owners_set:
			raise ValueError(
				f"User {u_id} is not an owner of channel {self._id}")
		# Update self and user
		get_user(u_id).get_channels().discard(self._id)
		self._owners_set.discard(u_id)
