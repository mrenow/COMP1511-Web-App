
"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request
from objects import *
import jwt
from AccessError import AccessError

users = {} # u_id: user obj
channels = {} # chann
messages = {} # message_id: message obj

private_key = "secure password"

def authcheck(u_id, user = None, channel = None, chowner = False, admin = False):
    
    if user != None and user != u_id:
        raise AccessError(f"auth: User {u_id} is not {user}.")
    if channel != None and not users[u_id].is_admin:
        if channel not in users[user].get_channels():+
            raise AccessError(f"auth: User {u_id} is not in channel {channel}")
        if chowner and user not in channels[channel].get_owners():
            raise AccessError(f"auth: User {u_id} is in channel {channel} but is not an owner.")  
    if admin and not users[u_id].is_admin():
        raise AccessError(f"auth: User {u_id} is not admin")

def tokcheck(token):
    try:
        payload = jwt.decode(token, private_key)
        return payload["u_id"]
    except (jwt.InvalidTokenError):
        return None



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


APP = Flask(__name__)
CORS(APP)

@APP.route('/auth/register', methods=['POST'])
def echo4():
    pass

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })




@APP.route()
def auth_login(email, password):
    return {}



@APP.route('/echo/get', methods=['GET'])
def auth_logout(token):
    return {}

@APP.route('/echo/get', methods=['GET'])
def auth_register(email, password, name_first, name_last):
    return {}

@APP.route('/echo/get', methods=['GET'])
def auth_passwordreset_request(email):
    return {}

@APP.route('/echo/get', methods=['GET'])
def auth_passwordreset_reset(reset_code, new_password):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channel_invite(token, channel_id, u_id):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channel_details(token, channel_id):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channel_messages(token, channel_id, start):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channel_leave(token, channel_id):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channel_join(token, channel_id):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channel_addowner(token, channel_id, u_id):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channel_removeowner(token, channel_id, u_id):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channels_list(token):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channels_listall(token):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channels_create(token, name, is_public):
    return {}

@APP.route('/echo/get', methods=['GET'])
def channels_delete(token, channel_id):
    return {}

@APP.route('/echo/get', methods=['GET'])
def message_sendlater(token, channel_id, message, time_sent):
    return {}

@APP.route('/message/send', methods=['GET'])
def message_send():
    
    u_id = tok(token)
    
    authcheck(u_id, channel = channel_id)
    channels[channel].send_message(u_id, message)


    return {}

@APP.route('/echo/get', methods=['GET'])
def send_message(user, message):
    authcheck(user, channel = self._channel_id)

@APP.route('/echo/get', methods=['GET'])
def message_remove(token, message_id):
    return {}
    
@APP.route('/echo/get', methods=['GET'])
def message_edit(token, message_id, message):
    return {}

@APP.route('/message/react', methods=['GET'])
def message_react(token, message_id, react_id): 
    
    if react in self._reacts and user in self._reacts.get(react)._u_ids:
            raise ValueError(f"message_react: User {user} already has react_id {react} on message {self._message_id}: '{self._message[:10]}...'")
     
    return {}
def message_unreact(token, message_id, react_id):



    if react not in self._reacts or user not in self._reacts.get(react)._u_ids:
            raise ValueError(f"message_unreact: User {user} already has react_id {react} on message {self._message_id}: '{self._message[:10]}...'")
        
    return {}

@APP.route('/echo/get', methods=['GET'])
def message_pin(token, message_id):        
    
    
    if self._is_pinned:
        raise ValueError(f"message.pin: Message {self._message_id} '{self._message[:10]}...' is already pinned.")
    else:
    return {}

@APP.route('/echo/get', methods=['GET'])
def message_unpin(token, message_id):
    if self._is_pinned:
        raise ValueError(f"message.unpin: Message {self._message_id} '{self._message[:10]}...' is not pinned.")
    else:
    
    return {}

@APP.route('/echo/get', methods=['GET'])
def user_profile(token, u_id):
    

    return {}
@APP.route('/echo/get', methods=['GET'])
def user_profile_setname(token, name_first, name_last):
    return {}
@APP.route('/echo/get', methods=['GET'])
def user_profile_setemail(token, email):
    return {}
@APP.route('/echo/get', methods=['GET'])
def user_profile_sethandle(token, handle_str):
    return {}
@APP.route('/echo/get', methods=['GET'])
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    return {}
@APP.route('/echo/get', methods=['GET'])
def standup_start(token, channel_id):
    return {}
@APP.route('/echo/get', methods=['GET'])
def standup_send(token, channel_id, message):
    return {}
@APP.route('/echo/get', methods=['GET'])
def search(token, query_str):
    return {}

@APP.route('/echo/get', methods=['GET'])
def admin_userpermission_change(token, u_id, permission_id):
    return {}


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))