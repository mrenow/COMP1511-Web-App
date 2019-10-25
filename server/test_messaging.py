import time
import pytest
from datetime import datetime, timedelta
from server.AccessError import AccessError
from server.server import *

# for index < 50
def get_message_id(token, channel, index):
    return channel_messages(token, channel, start = 0)["messages"][index]["message_id"]

# Creates an environment where a user and admin are members of a channel
def message_env():
    auth_response = auth_register("admin@email.com", "adminpass", "first", "last")
    admintok, admin = auth_response["token"], auth_response["u_id"]
    
    auth_response = auth_register("user@email.com", "userpass", "first", "last")
    usertok, user = auth_response["token"], auth_response["u_id"]

    channel = channels_create(admintok, "channel1", True)

    channel_join(usertok, channel)
    channel_join(admintok, channel)

    return admintok, admin, usertok, user, channel

# Adds an owner to the specified channel
def channel_owner_env(admintok, channel):
    auth_response = auth_register("owner@email.com", "ownerpass", "first", "last")
    ownertok, owner = auth_response["token"], auth_response["u_id"]

    channel_addowner(admintok, channel, owner)
    return ownertok, owner

# Adds a regular member with no permissions
def extra_member_env(id):
    auth_response = auth_register(f"user{id}@email.com", f"user{id}pass", "first", "last")
    return auth_response["token"], auth_response["u_id"]


def ms_offset(milliseconds):
    return datetime.now() + timedelta(milliseconds = milliseconds)
    
def assert_message(token, channel, messages, users, start = 0):
    message_response = channel_messages(token, channel, start = start)
    message_list, list_start, list_end = message_response["messages"], message_response["start"], message_response["end"] 
    # Check lengths
    assert start == list_start
    if list_end == -1:
        assert len(message_list) < 50
    else:
        assert list_end == start + 50

    assert len(message_list) <= 50, "Channel messages returned too many entries"
    assert len(message_list) == len(messages) == len(users), f"Length mismatch:\n exp {(messages, users)}\n got {message_list}"
    # Check content
    for got, message_exp, user_exp in zip(message_list, messages, users):
        assert got["messages"] == message_exp, f"Message mismatch: exp {message_exp} got {got['message']}"
        assert got["u_id"] == user_exp, f"User mismatch: exp {user_exp} got {got['u_id']}"
    # Check times
    for curr, nxt in zip(message_list[:-1], message_list[1:]):
        assert curr["time_created"] <= nxt["time_created"]

# Tests that the correct number of messages is displayed
def test_channel_messages():
    admintok, admin, usertok, user, channel = message_env()
    for _ in range(50):
        message_send(usertok, channel, "SPAM")

    assert_message(admintok, channel, ["SPAM"]*50, [user]*50)
    for _ in range(50):
        message_send(admintok, channel, "PROFANITY")

    assert_message(admintok, channel, ["SPAM"]*50, [user]*50, start = 50)
    assert_message(admintok, channel, ["PROFANITY"]*25 + ["SPAM"]*25, [admin]*25 + [user]*25, start = 25)

    private_channel = channels_create(admintok, "shhhh", is_public = False)

    # Cannot access private channel
    with pytest.raises(AccessError):
        channel_messages(usertok, private_channel, start = 0)
    
    # Start out of bounds.
    with pytest.raises(ValueError):
        channel_messages(admintok, private_channel, start = 1)
    with pytetest_st.raises(ValueError):
        channel_messages(admintok, channel, start = 101)

def test_message_limit_test():
    admintok, admin, usertok, user, channel = message_env()

    # Send is valid
    message_send(usertok, channel, TEST_VALID_MESSAGE)
    # Send is invalid
    with pytest.raises(ValueError):
        message_send(admintok, channel, TEST_INVALID_MESSAGE)
    # Edit is invalid
    m_id = channel_messages(admintok, channel, start = 0)["messages"][0]["message_id"]
    with pytest.raises(ValueError):
        message_edit(usertok, m_id, TEST_INVALID_MESSAGE)
    

    
    

# Tests message order, user id on message
def test_send_test():
    admintok, admin, usertok, user, channel = message_env()

    message_send(usertok, channel, "testing")
    assert_message(admintok, channel, ["testing"], [user])
    message_send(admintok, channel, "testing")
    assert_message(admintok, channel, ["testing", "testing"], [admin, user])
    message_send(usertok, channel, "one")
    assert_message(admintok, channel, ["one", "testing", "testing"],  [user, admin, user])
    message_send(usertok, channel, "two")
    assert_message(admintok, channel, ["two", "one", "testing", "testing"], [user, user, admin, user])
    message_send(admintok, channel, "three")
    assert_message(admintok, channel, ["three", "two", "one", "testing", "testing"], [admin, user, user, admin, user])

    # Bad channel
    with pytest.raises(ValueError):
        message_send(admintok, -1, "sudo rm -rf")

    user1tok, user1 = extra_member_env(1)
    # Not in channel
    with pytest.raises(AccessError):
        message_send(user1tok, channel, "can i have mod")
    

# Tests message order on send later
def test_send_later_test():
    admintok, admin, usertok, user, channel = message_env()
    user1tok, user1 = extra_member_env(1)

    message_send(usertok, channel, "1")
    message_sendlater(admintok, channel, "2", ms_offset(1600))
    message_sendlater(usertok, channel, "3", ms_offset(800))
    message_send(admintok, channel, "4")
    
    assert_message(admintok, channel, ["4", "1"], [admin, user])
    time.sleep(0.6)
    assert_message(admintok, channel, ["4", "1"], [admin, user])
    time.sleep(0.3)
    assert_message(admintok, channel, ["3", "4", "1"], [user, admin, user])
    time.sleep(0.8)
    assert_message(admintok, channel, ["2", "3", "4", "1"], [admin, user, admin, user])

    # Bad channel
    with pytest.raises(ValueError):
        message_sendlater(admintok, -1, "sudo rm -rf", ms_offset(100))
    # Bad time
    with pytest.raises(ValueError):
        message_sendlater(admintok, channel, "One day, I, the admin, will superceed time itself", ms_offset(-10))

    # Not in channel
    with pytest.raises(AccessError):
        message_sendlater(user1tok, channel, "can i have mod", ms_offset(100))

def test_edit_message_test():
    admintok, admin, usertok, user, channel = message_env()
    ownertok, owner = channel_owner_env(admintok,channel)
    user1tok, user1 = extra_member_env(1)
    channel_join(user1tok, channel)

    message_send(admintok, channel, "1")
    message_send(usertok, channel, "2")
    message_send(ownertok, channel, "3")
    message_send(user1tok, channel, "4")
    
    initial_messages = channel_messages(admintok, channel, start = 0)["messages"]

    # Valid edits on user
    message_edit(admintok, initial_messages[0]["message_id"], "a")
    assert_message(admintok, channel, ["a", "3", "2", "1"], [user1, owner, user, admin])
    message_edit(user1tok, initial_messages[0]["message_id"], "b")
    assert_message(admintok, channel, ["b", "3", "2", "1"], [user1, owner, user, admin])
    message_edit(ownertok, initial_messages[0]["message_id"], "c")
    assert_message(admintok, channel, ["c", "3", "2", "1"], [user1, owner, user, admin])
    
    # valid edits on admin
    message_edit(ownertok, initial_messages[3]["message_id"], "d")
    assert_message(admintok, channel, ["b", "3", "2", "d"], [user1, owner, user, admin])
    message_edit(admintok, initial_messages[3]["message_id"], "e")
    assert_message(admintok, channel, ["c", "3", "2", "e"], [user1, owner, user, admin])

    # Invalid because of user mismatch
    with pytest.raises(ValueError):
        message_edit(usertok, initial_messages[1]["message_id"], "Stop!")
    with pytest.raises(ValueError):
        message_edit(usertok, initial_messages[3]["message_id"], "You violated the law.") 
    
    # Invalid because message does not exist
    with pytest.raises(ValueError):
        message_edit(admintok, -1, "something happened:")
    with pytest.raises(ValueError):
        message_edit(ownertok, -1, "something happened") 
    
    # Invalid permissions
    with pytest.raises(AccessError):
        message_edit(usertok, initial_messages[0]["message_id"], "Segmentation")
    with pytest.raises(AccessError):
        message_edit(usertok, initial_messages[1]["message_id"], "fault")
    with pytest.raises(AccessError):
        message_edit(usertok, initial_messages[3]["message_id"], "(core dumped)")
    

    # Not in channel
    channel_leave(admintok, channel)
    with pytest.raises(AccessError):
        message_edit(admintok, initial_messages[3], "I wuz here")

    # Assert that edits did not go through
    assert_message(admintok, channel, ["c", "3", "2", "e"], [user, owner, user, admin])
    
    
#assert_message(admintok, channel, ["0","1","2","3","4","5","6","7","8"],  [owner]*3 + [user]*3 + [admin]*3)
    
def test_remove_message_test():
    admintok, admin, usertok, user, channel = message_env()
    ownertok, owner = channel_owner_env(admintok,channel)
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
    assert_message(admintok, channel, ["0","1","2","3","4","5","7","8"], [owner]*3 + [user]*3 + [admin]*2)
    
    message_remove(admintok, message_ids[1])
    with pytest.raises(ValueError):
        message_remove(admintok, message_ids[1])   
    assert_message(admintok, channel, ["0","2","3","4","5","7","8"], [owner]*2 + [user]*3 + [admin]*2)
    
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
    assert_message(admintok, channel, ["0","2","3","4","5","7","8"], [owner]*2 + [user]*3 + [admin]*2)

def test_pin_test():
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
def test_standup_test():
    admintok, admin, usertok, user, channel = message_env()
    channel_leave(admintok, channel)
    
    # Not in channel
    with pytest.raises(AccessError):
        standup_start(admintok, channel)

    # Invalid because no standup in session
    with pytest.raises(AccessError):
        standup_send(admintok, channel, "standup")

    channel_join(admintok, channel)

    finish = standup_start(admintok, channel)["time_finish"]
    # Cannot start two standups
    with pytest.raises(ValueError):
        standup_start(admintok, channel)["time_finish"]
    
    # Finish time to be in 15 minutes +- 5 seconds
    assert timedelta(seconds = -5) < finish - (datetime.now() + timedelta(minutes=15)) < timedelta(seconds = 5)
    
    standup_send(usertok, channel, "I walked my dog")
    standup_send(admintok, channel, "I stayed up till 4 am redefining specifications")
    assert_message(admintok, channel, ["I stayed up till 4 am redefining specifications", "I walked my dog"], [user, admin])
    
    with pytest.raises(ValueError):
        standup_send(admintok, channel, TEST_INVALID_MESSAGE)
    standup_send(admintok, channel, TEST_VALID_MESSAGE)

    channel_leave(admintok, channel)
        
    # Not in channel
    with pytest.raises(AccessError):
        standup_send(admintok, channel, "not part of yo club anymo")

    # Check that messages unchanged
    assert_message(admintok, channel, ["I stayed up till 4 am redefining specifications", "I walked my dog"], [user, admin])
    
    # Bad channel_id
    with pytest.raises(ValueError):
        standup_send(admintok, -1, TEST_INVALID_MESSAGE)
    with pytest.raises(ValueError):
        standup_start(admintok, -1)



# Not enough specification to test react:
#   - Where does the react ID come from?
#   - Do different users have different react IDs for the same react?
#   - Is there more than one react? (Hayden's video says there only likes are being used)
#   - Can multiple users react the same message? Should there be some way to count reacts?
''' TODO:
def react_message_test():
    admintok, admin, usertok, user, channel = message_env()
    ownertok, owner = channel_owner_env(admintok,channel)

    message_send(admintok, channel, "1")
    message_send(usertok, channel, "2")
    message_send(ownertok, channel, "3")
    message_send(usertok, channel, "4")

    message_react(usertok, channel, )
'''

# Not enough specifications to test search:
#   - What counts as "matching the query"?

    

