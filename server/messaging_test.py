import time
import pytest
from datetime import datetime, timedelta


from AccessError import AccessError
from server import *


def message_env():
    auth_response = auth_register("admin@email.com", "admin", "first", "last")
    admintok, admin = auth_response["token"], auth_response["u_id"]
    
    auth_response = auth_register("user@email.com", "user", "first", "last")
    usertok, user = auth_response["token"], auth_response["u_id"]

    channel = channels_create(admintok, "channel1", True)
    channel_join(usertok, channel)
    channel_join(admintok, channel)
    


    return admintok, admin, usertok, user, channel

def channel_owner_env(admintok, channel):
    auth_response = auth_register("owner@email.com", "owner", "first", "last")
    ownertok, owner = auth_response["token"], auth_response["u_id"]

    channel_addowner(admintok, channel, owner)
    return ownertok, owner


def ms_offset(milliseconds):
    return datetime.now() + timedelta(milliseconds = milliseconds)
    
def assert_message(token, channel, messages, users):
    message_response = channel_messages(token, channel, start = 0)["messages"]
    # Check lengths
    assert len(message_response) <= 50, "Channel messages returned too many entries"
    assert len(message_response) == len(messages) == len(users), f"Length mismatch:\n exp {(messages, users)}\n got {message_response}"
    # Check content
    for got, message_exp, user_exp in zip(message_response, messages, users):
        assert got["messages"] == message_exp, f"Message mismatch: exp {message_exp} got {got['message']}"
        assert got["u_id"] == user_exp, f"User mismatch: exp {user_exp} got {got['u_id']}"
    # Check times
    for curr, nxt in zip(message[:-1], message[1:]):
        assert curr["time_created"] <= nxt["time_created"]

def channel_messages_test():
    admintok, admin, usertok, user, channel = message_env()
    for _ in range(50):
        message_send(usertok, channel, "SPAM")

    assert len(channel_messages(admintok, channel, start = 0)["messages"])

    

# Tests message order, user id on message
def send_test():
    admintok, admin, usertok, user, channel = message_env()

    message_send(usertok, channel, "testing")
    assert_messages(admintok, channel, ["testing"], [user])
    message_send(admintok, channel, "testing")
    assert_messages(admintok, channel, ["testing", "testing"], [user, admin])
    message_send(usertok, channel, "one")
    assert_messages(admintok, channel, ["testing", "testing", "one"],  [user, admin, user])
    message_send(usertok, channel, "two")
    assert_messages(admintok, channel, ["testing", "testing", "one", "two"], [user, admin, user, user])
    message_send(admintok, channel, "three")
    assert_messages(admintok, channel, ["testing", "testing", "one", "two", "three"], [user, admin, user, user, admin])

# Tests message order on send later
def send_later_test():
    admintok, admin, usertok, user, channel = message_env()

    message_send(usertok, channel, "1")
    message_sendlater(admintok, channel, "2", ms_offset(1600))
    message_sendlater(usertok, channel, "3", ms_offset(800))
    message_send(admintok, channel, "4")
    
    assert_message(admintok, channel, ["1", "4"], [user, admin])
    time.sleep(0.6)
    assert_message(admintok, channel, ["1", "4"], [user, admin])
    time.sleep(0.3)
    assert_message(admintok, channel, ["1", "4", "3"], [user, admin, user])
    time.sleep(0.8)
    assert_message(admintok, channel, ["1", "4", "3", "2"], [user, admin, user, admin])

def edit_message_test():
    admintok, admin, usertok, user, channel = message_env()
    ownertok, owner = channel_owner_env(admintok,channel)

    message_send(admintok, channel, "1")
    message_send(usertok, channel, "2")
    message_send(admintok, channel, "3")
    message_send(usertok, channel, "4")
    
    initial_messages = channel_messages(admintok, channel, start = 0)["messages"]

    # Valid edits
    message_edit(admintok, channel, initial_messages[0]["message_id"], "1")
    message_edit(usertok, channel, initial_messages[3]["message_id"], "1")

    # Invalid because of user mismatch
    with pytest.raises(ValueError):
        message_edit(admintok, channel, initial_messages[1]["message_id"], "Stop!")
    with pytest.raises(ValueError):
        message_edit(usertok, channel, initial_messages[2]["message_id"], "You violated the law.")

    

