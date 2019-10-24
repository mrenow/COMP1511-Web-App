import sys
from json import dumps
from flask import Flask, request


users = {} # u_id: user obj
channels = {} # chann
messages = {} # message_id: message obj

from objects.messages import Message
from objects.channels_object import Channel
import jwt
from server.AccessError import AccessError


private_key = "secure password"


'''
Raises an Access error if all of the conditions specified are not met.
Usage:
Only allow if is ( owner of channel or admin or particular user ) and in channel:
>>> authcheck(u_id, user = particular_u_id, chowner = channel_id,  admin = True)
>>> authcheck(u_id, user = channel_id) 
'''
def authcheck(u_id, user = None, channel = None, chowner = None, admin = False):
    auth = False 

    if user != None and user == u_id:
        auth = True
    if channel != None and channel in users[user].get_channels():
        auth = True
    if chowner != None and user in channels[chowner].get_owners():
        auth = True
    if admin and users[u_id].is_admin():
        auth = True
    if auth:
        return
    
    if user != None:
        raise AccessError(f"auth: User {u_id} is not user {user}.")
    if channel != None:
        raise AccessError(f"auth: User {u_id} is not in channel {channel}")
    if chowner != None:
        raise AccessError(f"auth: User {u_id} is not an owner of {channel}.")  
    if admin:
        raise AccessError(f"auth: User {u_id} is not admin")



def tokcheck(token):
    payload = jwt.decode(token, private_key)
    return payload["u_id"]



TEST_OWNER_EMAIL = "TODO"
TEST_OWNER_PASSWORD = "TODO"
TEST_CHANNEL_EMAIL = "TODO"
TEST_CHANNEL_PASSWORD = "TODO"
TEST_EMAIL = "TODO"
TEST_PASSWORD = "TODO"
TEST_CHANNEL_OWNER_UID = "TODO"
TEST_NORMAL_UID = "TODO"
TEST_INVALID_UID = "TODO"
TEST_INVALID_PASSWORD = TEST_PASSWORD + " "
TEST_INVALID_EMAIL = "TODO"
TEST_INVALID_MESSAGE = "0"*1001
TEST_VALID_MESSAGE = "0"*1000
TEST_VALID_CHANNEL_ID = "TODO"  
TEST_INVALID_CHANNEL_ID = "TODO"
TEST_VALID_CHANNEL_OWNER = "TODO"

TEST_VALID_REACT = 0


def auth_login(email, password):
    return {}
def auth_logout(token):
    return {}
def auth_register(email, password, name_first, name_last):
    return {}
def auth_passwordreset_request(email):
    return {}
def auth_passwordreset_reset(reset_code, new_password):
    return {}
def channel_invite(token, channel_id, u_id):
    requester = tokcheck(token) 
    if channel_id not in channels:
        raise ValueError((f"channel_invite: Channel does not exist."))
    if u_id not in users:
        raise ValueError((f"channel_invite: User does not exist."))
    if requester not in channels[channel_id].get_members():
        raise AccessError((f"auth: User is not a member of this channel"))
    
    channels[channel_id].join(u_id)
    
    return {}
def channel_details(token, channel_id):
    return {}
def channel_messages(token, channel_id, start): 
    u_id = tokcheck



    return 
def channel_leave(token, channel_id):
    return {}
def channel_join(token, channel_id):
    return {}
def channel_addowner(token, channel_id, u_id):
    return {}
def channel_removeowner(token, channel_id, u_id):
    return {}

def channels_list(token):
    u_id = tok(token)
    authcheck(u_id, channel = channel_id)
    
    return {}
def channels_listall(token):
    u_id = tok(token)
    authcheck(u_id, channel = channel_id)
    
    return {}
def channels_create(token, name, is_public):
    u_id = tok(token)
    authcheck(u_id, channel = channel_id)
    
    return {}

'''
Added to the specification.
'''

def channels_delete(token, channel_id):
    u_id = tokcheck(token)
    authcheck(u_id, channel = channel_id)
    
    return {}

def message_sendlater(token, channel_id, message, time_sent):
    
    return {}


'''
Ezra: done
'''
def message_send(token, channel_id, message): 
    u_id = tokcheck(token)
    authcheck(u_id, channel = channel_id)
    channels[channel_id].send_message(u_id, message)

    return {}

'''
Ezra: done 
'''
def message_remove(token, message_id):
    u_id = tokcheck(token)
    mess = messages[message_id]
    authcheck(u_id, channel = mess.get_id())
    authcheck(u_id, user = mess.get_user(), chowner = mess.get_channel(), admin = True)
    mess.remove()
    return {}


'''
Ezra: done 
'''
def message_edit(token, message_id, message):
    u_id = tokcheck(token)
    mess = messages[message_id]
    authcheck(u_id, channel = mess.get_id())
    authcheck(u_id, user = mess.get_user(), chowner = mess.get_channel(), admin = True)
    mess.set_message(message)
    return {}

'''
Ezra: done 
'''
def message_react(token, message_id, react_id): 
    u_id = tokcheck(token)
    mess = messages[message_id]
    authcheck(u_id, channel = mess.get_id())
    
    if react_id in mess.get_reacts() and u_id in mess._reacts.get(react_id).get_users():
        raise ValueError(f"message_react: User {u_id} already has react_id {react_id} on message {mess.get_id()}: '{mess.get_message()[:10]}...'")
    mess.add_react(u_id, react_id)
    
    return {}

'''
Ezra: done 
'''
def message_unreact(token, message_id, react_id):
    u_id = tokcheck(token)
    mess = messages[message_id]
    authcheck(u_id, channel = mess.get_id())

    if react_id not in mess.get_reacts():
        raise ValueError(f"message_unreact: React_id {react_id} not on message {mess.get_id()}: '{mess.get_message()[:10]}...'")
       
    if u_id not in mess._reacts.get(react_id).get_users():
        raise ValueError(f"message_unreact: User {u_id} does not have react_id {react_id} on message {mess.get_id()}: '{mess.get_message()[:10]}...'")
    
    mess.remove_react(u_id, react_id)
    
    return {}

'''
Ezra: done 
'''
def message_pin(token, message_id):        
    u_id = tokcheck(token)
    mess = messages[message_id]
    authcheck(u_id, chowner = mess.get_channel(), admin = True)
    
    if mess.is_pinned():
        raise ValueError(f"message_pin: Message {mess.get_id()} '{mess.get_message()[:10]}...' is already pinned.")
    mess.set_pin(True)
    
    return {}

'''
Ezra: done 
'''
def message_unpin(token, message_id):   
    u_id = tokcheck(token)
    mess = messages[message_id]
    authcheck(u_id, chowner = mess.get_channel(), admin = True)
    
    if mess.is_pinned():
        raise ValueError(f"message_unpin: Message {mess.get_id()} '{mess.get_message()[:10]}...' is not pinned.")
    mess.set_pin(False)
    
    return {}
def user_profile(token, u_id):
    

    return {}
def user_profile_setname(token, name_first, name_last):
    return {}
def user_profile_setemail(token, email):
    return {}
def user_profile_sethandle(token, handle_str):
    return {}
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    return {}
def standup_start(token, channel_id):
    return {}
def standup_send(token, channel_id, message):
    return {}
def search(token, query_str):
    return {}
def admin_userpermission_change(token, u_id, permission_id):
    return {}