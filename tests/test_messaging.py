import time
import pytest
from datetime import datetime, timedelta
from server.AccessError import AccessError
from server.constants import *
from server.state import *

from server.channel import *
from server.message import *
from server.auth import *
from server.standup import *

TEST_INVALID_MESSAGE = "0"*1001
TEST_VALID_MESSAGE = "0"*1000


@pytest.fixture
def clear():
	reset()

# for index < 50


def get_message_id(token, channel, index):
	return channel_messages(token, channel, start=0)["messages"][index]["message_id"]

# Creates an environment of a admin (channel owner) and a user in one channel


def message_env():
	global _users, _channels, _messages
	auth_response = auth_register(
		"admin@email.com", "adminpass", "afirst", "alast")
	admintok, admin = auth_response["token"], auth_response["u_id"]

	auth_response = auth_register(
		"user@email.com", "userpass", "ufirst", "ulast")
	usertok, user = auth_response["token"], auth_response["u_id"]

	channel = channels_create(admintok, "channel1", is_public=True)[
		"channel_id"]

	channel_join(usertok, channel)
	channel_join(admintok, channel)

	return admintok, admin, usertok, user, channel

# Adds an owner to the specified channel


def channel_owner_env(admintok, channel):
	auth_response = auth_register(
		"owner@email.com", "ownerpass", "ofirst", "olast")
	ownertok, owner = auth_response["token"], auth_response["u_id"]

	channel_addowner(admintok, channel, owner)
	return ownertok, owner

# Adds a regular member with no permissions


def extra_member_env(id):
	auth_response = auth_register(
		f"user{id}@email.com", f"user{id}pass", f"u{id}first", f"u{id}last")
	return auth_response["token"], auth_response["u_id"]


def ms_offset(milliseconds):
	return datetime.now(TIMEZONE) + timedelta(milliseconds=milliseconds)


def extract_messages(message_list):
	return [mess['message'] for mess in message_list]


def extract_users(message_list):
	return [mess['u_id'] for mess in message_list]


def assert_message(token, channel, messages, users, start=0):
	message_response = channel_messages(token, channel, start=start)
	message_list, list_start, list_end = message_response[
		"messages"], message_response["start"], message_response["end"]
	# Check lengths
	assert start == list_start

	if (len(message_list) == 50):
		next_response = channel_messages(token, channel, start=start+1)
		if (len(next_response["messages"]) < 50):
			assert list_end == - \
				1, f"Current response has 50 messages and takes the last message from the channel. message_list: {len(message_list)}, next : {len(next_response['messages'])}"
		else:
			assert list_end != -1
	else:
		assert list_end == -1
	if list_end != -1:
		assert list_end == start + 50

	assert len(message_list) <= 50, "Channel messages returned too many entries"
	assert len(message_list) == len(messages) == len(
		users), f"Length mismatch:\n exp {(messages, users)}\n got {message_list}\n{message_list}"
	# Check content
	for got, message_exp, user_exp in zip(message_list, messages, users):
		assert got[
			"message"] == message_exp, f"Message mismatch: exp {messages} got {extract_messages(message_list)}\n{message_list}"
		assert got[
			"u_id"] == user_exp, f"User mismatch: exp {users} got {extract_users(message_list)}"
	# Check times
	for curr, nxt in zip(message_list[:-1], message_list[1:]):
		assert curr["time_created"] >= nxt["time_created"]

# Tests that the correct number of messages is displayed


def test_channel_messages(clear):
	admintok, admin, usertok, user, channel = message_env()
	for _ in range(50):
		message_send(usertok, channel, "SPAM")

	assert_message(admintok, channel, ["SPAM"]*50, [user]*50)
	for _ in range(50):
		message_send(admintok, channel, "PROFANITY")

	assert_message(admintok, channel, ["SPAM"]*50, [user]*50, start=50)
	assert_message(admintok, channel, [
            "PROFANITY"]*25 + ["SPAM"]*25, [admin]*25 + [user]*25, start=25)

	private_channel = channels_create(
		admintok, "shhhh", is_public=False)["channel_id"]

	# Cannot access private channel
	with pytest.raises(AccessError):
		channel_messages(usertok, private_channel, start=0)

	# Start out of bounds.
	with pytest.raises(ValueError):
		channel_messages(admintok, private_channel, start=1)
	with pytest.raises(ValueError):
		channel_messages(admintok, channel, start=101)


def test_message_limit(clear):
	admintok, admin, usertok, user, channel = message_env()

	# Send is valid
	message_send(usertok, channel, TEST_VALID_MESSAGE)
	# Send is invalid
	with pytest.raises(ValueError):
		message_send(admintok, channel, TEST_INVALID_MESSAGE)
	# Edit is invalid
	m_id = channel_messages(admintok, channel, start=0)[
		"messages"][0]["message_id"]
	with pytest.raises(ValueError):
		message_edit(usertok, m_id, TEST_INVALID_MESSAGE)


# Tests message order, user id on message
def test_send(clear):
	admintok, admin, usertok, user, channel = message_env()

	message_send(usertok, channel, "testing")
	assert_message(admintok, channel, ["testing"], [user])
	message_send(admintok, channel, "testing")
	assert_message(admintok, channel, ["testing", "testing"], [admin, user])
	message_send(usertok, channel, "one")
	assert_message(admintok, channel, [
            "one", "testing", "testing"],  [user, admin, user])
	message_send(usertok, channel, "two")
	assert_message(admintok, channel, ["two", "one", "testing", "testing"], [
            user, user, admin, user])
	message_send(admintok, channel, "three")
	assert_message(admintok, channel, ["three", "two", "one", "testing", "testing"], [
            admin, user, user, admin, user])

	# Bad channel
	with pytest.raises(ValueError):
		message_send(admintok, -1, "sudo rm -rf")

	user1tok, user1 = extra_member_env(1)
	# Not in channel
	with pytest.raises(AccessError):
		message_send(user1tok, channel, "can i have mod")


# Tests message order on send later
def test_send_later(clear):
	admintok, admin, usertok, user, channel = message_env()
	user1tok, user1 = extra_member_env(1)

	message_send(usertok, channel, "1")
	print("beep")
	message_sendlater(admintok, channel, "2", ms_offset(1600))
	message_sendlater(usertok, channel, "3", ms_offset(800))
	message_send(admintok, channel, "4")

	assert_message(admintok, channel, ["4", "1"], [admin, user])
	time.sleep(0.6)
	assert_message(admintok, channel, ["4", "1"], [admin, user])
	time.sleep(0.3)
	assert_message(admintok, channel, ["3", "4", "1"], [user, admin, user])
	time.sleep(0.8)
	assert_message(admintok, channel, ["2", "3", "4", "1"], [
            admin, user, admin, user])

	# Bad channel
	with pytest.raises(ValueError):
		message_sendlater(admintok, -1, "sudo rm -rf", ms_offset(100))
	# Bad time
	with pytest.raises(ValueError):
		message_sendlater(
			admintok, channel, "One day, I, the admin, will superceed time itself", ms_offset(-10))

	# Not in channel
	with pytest.raises(AccessError):
		message_sendlater(user1tok, channel, "can i have mod", ms_offset(100))


def test_edit_message(clear):
	admintok, admin, usertok, user, channel = message_env()
	ownertok, owner = channel_owner_env(admintok, channel)
	user1tok, user1 = extra_member_env(1)
	channel_join(user1tok, channel)

	message_send(admintok, channel, "1")
	message_send(usertok, channel, "2")
	message_send(ownertok, channel, "3")
	message_send(user1tok, channel, "4")

	initial_messages = channel_messages(admintok, channel, start=0)["messages"]

	# Valid edits on user
	message_edit(admintok, initial_messages[0]["message_id"], "a")
	assert_message(admintok, channel, ["a", "3", "2", "1"], [
            user1, owner, user, admin])
	message_edit(user1tok, initial_messages[0]["message_id"], "b")
	assert_message(admintok, channel, ["b", "3", "2", "1"], [
            user1, owner, user, admin])
	message_edit(ownertok, initial_messages[0]["message_id"], "c")
	assert_message(admintok, channel, ["c", "3", "2", "1"], [
            user1, owner, user, admin])

	# valid edits on admin
	message_edit(ownertok, initial_messages[3]["message_id"], "d")
	assert_message(admintok, channel, ["c", "3", "2", "d"], [
            user1, owner, user, admin])
	message_edit(admintok, initial_messages[3]["message_id"], "e")
	assert_message(admintok, channel, ["c", "3", "2", "e"], [
            user1, owner, user, admin])

	# Empty edit deletes message
	message_edit(ownertok, initial_messages[2]["message_id"], "")
	assert_message(admintok, channel,  ["c", "3", "e"], [user1, owner, admin])

	# Invalid because of user mismatch
	with pytest.raises(AccessError):
		message_edit(usertok, initial_messages[1]["message_id"], "Stop!")
	with pytest.raises(AccessError):
		message_edit(
			usertok, initial_messages[3]["message_id"], "You violated the law.")

	# Invalid because message does not exist
	with pytest.raises(ValueError):
		message_edit(admintok, -1, "something happened:")
	with pytest.raises(ValueError):
		message_edit(ownertok, -1, "something happened")

	# Invalid permissions
	with pytest.raises(AccessError):
		message_edit(
			usertok, initial_messages[0]["message_id"], "Segmentation")
	with pytest.raises(AccessError):
		message_edit(usertok, initial_messages[1]["message_id"], "fault")
	with pytest.raises(AccessError):
		message_edit(
			usertok, initial_messages[3]["message_id"], "(core dumped)")

	# Not in channel
	channel_leave(admintok, channel)
	with pytest.raises(AccessError):
		message_edit(admintok, initial_messages[3]["message_id"], "I wuz here")

	# Assert that edits did not go through
	assert_message(usertok, channel, ["c", "3", "e"], [user1, owner, admin])


#assert_message(admintok, channel, ["0","1","2","3","4","5","6","7","8"],  [owner]*3 + [user]*3 + [admin]*3)

def test_remove_message(clear):
	admintok, admin, usertok, user, channel = message_env()
	ownertok, owner = channel_owner_env(admintok, channel)
	print("TEST_CHANNEL", channel)
	user1tok, user1 = extra_member_env(1)
	channel_join(user1tok, channel)

	message_send(admintok, channel, "8")
	message_send(admintok, channel, "7")
	message_send(admintok, channel, "6")
	message_send(usertok, channel, "5")
	message_send(usertok, channel, "4")
	message_send(usertok, channel, "3")
	message_send(ownertok, channel, "2")
	message_send(ownertok, channel, "1")
	message_send(ownertok, channel, "0")

	message_ids = [get_message_id(admintok, channel, i) for i in range(9)]

	# Nonsense id
	with pytest.raises(ValueError):
		message_remove(ownertok, -1)

	# Removing an already removed message
	message_remove(ownertok, message_ids[6])
	with pytest.raises(ValueError):
		message_remove(ownertok, message_ids[6])
	assert_message(admintok, channel, ["0", "1", "2", "3", "4", "5", "7", "8"], [
            owner]*3 + [user]*3 + [admin]*2)

	message_remove(admintok, message_ids[1])
	print("message_id", message_ids[1])
	with pytest.raises(ValueError):
		message_remove(admintok, message_ids[1])
	assert_message(admintok, channel, ["0", "2", "3", "4", "5", "7", "8"], [
            owner]*2 + [user]*3 + [admin]*2)

	# Access denied
	with pytest.raises(AccessError):
		message_remove(usertok, message_ids[0])
	with pytest.raises(AccessError):
		message_remove(usertok, message_ids[8])
	with pytest.raises(AccessError):
		message_remove(user1tok, message_ids[4])

	# Not in channel
	channel_leave(admintok, channel)
	with pytest.raises(AccessError):
		message_remove(admintok, message_ids[4])

	# Assert removes did not go through
	assert_message(usertok, channel, ["0", "2", "3", "4", "5", "7", "8"], [
            owner]*2 + [user]*3 + [admin]*2)


def test_pin(clear):
	admintok, admin, usertok, user, channel = message_env()
	message_send(usertok, channel, "ello")

	message_pin(admintok, get_message_id(admintok, channel, 0))
	# Check if pinned
	with pytest.raises(ValueError):
		message_pin(usertok, get_message_id(admintok, channel, 0))
	# Also check if pinned (would raise value error otherwise)
	with pytest.raises(AccessError):
		message_unpin(usertok, get_message_id(admintok, channel, 0))

	message_unpin(admintok, get_message_id(admintok, channel, 0))
	# Check if unpinned
	with pytest.raises(ValueError):
		message_unpin(usertok, get_message_id(admintok, channel, 0))
	# Also check if unpinned (would raise value error otherwise)
	with pytest.raises(AccessError):
		message_pin(usertok, get_message_id(admintok, channel, 0))

	# Not in channel
	channel_leave(admintok, channel)
	with pytest.raises(AccessError):
		message_pin(admintok, get_message_id(admintok, channel, 0))

# To consider: how should remove, edit, etc function within a standup


def test_standup(clear):
	admintok, admin, usertok, user, channel = message_env()
	channel_leave(admintok, channel)

	assert standup_active(usertok, channel) == dict(
		is_active=False, time_finish=None)

	# Not in channel
	with pytest.raises(AccessError):
		standup_start(admintok, channel, 10)

	# Invalid because no standup in session
	with pytest.raises(AccessError):
		standup_send(admintok, channel, "standup")

	# Start standup
	channel_join(admintok, channel)
	finish = standup_start(admintok, channel, 3)["time_finish"]

	assert standup_active(usertok, channel) == dict(
		is_active=True, time_finish=finish.timestamp())

	# Cannot start two standups
	with pytest.raises(ValueError):
		standup_start(admintok, channel, 10)["time_finish"]

	# Finish time to be in 15 minutes +- 1 second
	assert timedelta(seconds=-1) < finish - (datetime.now(TIMEZONE) +
                                          timedelta(seconds=3)) < timedelta(seconds=1)

	standup_send(usertok, channel, "I walked my dog")
	standup_send(admintok, channel,
              "I stayed up till 4 am redefining specifications")

	# Bad message
	with pytest.raises(ValueError):
		standup_send(admintok, channel, TEST_INVALID_MESSAGE)
	standup_send(usertok, channel, TEST_VALID_MESSAGE)

	# Not in channel
	channel_leave(admintok, channel)
	with pytest.raises(AccessError):
		standup_send(admintok, channel, "not part of yo club anymo")

	# Check no messages have been sent
	assert_message(usertok, channel, [], [])
	message_send(usertok, channel, "I am a mongoose")
	assert_message(usertok, channel, ["I am a mongoose"], [user])

	time.sleep(3)
	assert_message(usertok, channel, [
            f"{STANDUP_START_STR}\nufirst: I walked my dog\nafirst: I stayed up till 4 am redefining specifications\nufirst: {TEST_VALID_MESSAGE}", "I am a mongoose"], [admin, user])

	# Bad channel_id
	with pytest.raises(ValueError):
		standup_send(admintok, -1, TEST_INVALID_MESSAGE)
	with pytest.raises(ValueError):
		standup_start(admintok, -1, 10)

# Checking that id = 1 only for iter 2


def assert_react(token, channel, index, users):
	reacts = channel_messages(token, channel, start=0)[
		"messages"][index]["reacts"]
	if len(reacts) == 0:
		return
	assert len(reacts) == 1
	assert reacts[0]["react_id"] == 1
	assert sorted(reacts[0]["u_ids"]) == sorted(users)


def error_react(reacted, unreacted, mess_id):
	for user in reacted:
		with pytest.raises(ValueError):
			message_react(user, mess_id, 1)
	for user in unreacted:
		with pytest.raises(ValueError):
			message_unreact(user, mess_id, 1)


def test_react_message(clear):
	admintok, admin, usertok, user, channel = message_env()
	ownertok, owner = channel_owner_env(admintok, channel)
	user1tok, user1 = extra_member_env(1)

	message_send(admintok, channel, "1")
	message_send(usertok, channel, "2")
	message_send(ownertok, channel, "3")
	message_send(usertok, channel, "4")

	message_ids = [get_message_id(admintok, channel, i) for i in range(4)]

	# Bad react id
	for i in range(10):
		if i == 1:
			continue
		with pytest.raises(ValueError):
			message_react(admintok, message_ids[3], i)

	# Adding reacts

	message_react(admintok, message_ids[3], 1)
	assert_react(admintok, channel, 3, [admin])
	error_react([admintok], [usertok, ownertok], message_ids[3])

	message_react(usertok, message_ids[3], 1)
	assert_react(usertok, channel, 3, [admin, user])
	error_react([admintok, usertok], [ownertok], message_ids[3])

	message_react(ownertok, message_ids[3], 1)
	assert_react(ownertok, channel, 3, [admin, user, owner])
	error_react([admintok, usertok, ownertok], [], message_ids[3])

	# removing reacts
	message_unreact(usertok, message_ids[3], 1)
	assert_react(admintok, channel, 3, [admin, owner])
	error_react([admintok,  ownertok], [usertok], message_ids[3])

	message_unreact(admintok, message_ids[3], 1)
	assert_react(admintok, channel, 3, [owner])
	error_react([ownertok], [admintok, usertok], message_ids[3])

	message_unreact(ownertok, message_ids[3], 1)
	assert_react(admintok, channel, 3, [])
	error_react([], [admintok, usertok, ownertok], message_ids[3])

	message_react(usertok, message_ids[1], 1)
	assert_react(admintok, channel, 1, [user])

	# User not in channel
	with pytest.raises(AccessError):
		message_react(user1tok, message_ids[2], 1)

	channel_leave(usertok, channel)
	with pytest.raises(AccessError):
		message_unreact(usertok, message_ids[1], 1)
