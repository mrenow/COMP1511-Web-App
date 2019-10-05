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
    return {}
def channel_details(token, channel_id):
    return {}
def channel_messages(token, channel_id, start):
    return {}
def channel_leave(token, channel_id):
    return {}
def channel_join(token, channel_id):
    return {}
def channel_addowner(token, channel_id, u_id):
    return {}
def channel_removeowner(token, channel_id, u_id):
    return {}
def channels_list(token):
    return {}
def channels_listall(token):
    return {}
def channels_create(token, name, is_public):
    return {}
def message_sendlater(token, channel_id, message, time_sent):
    return {}
def message_send(token, channel_id, message):
    return {}
def message_remove(token, message_id):
    return {}
def message_edit(token, message_id, message):
    return {}
def message_react(token, message_id, react_id):
    return {}
def message_unreact(token, message_id, react_id):
    return {}
def message_pin(token, message_id):
    return {}
def message_unpin(token, message_id):
    return {}
def user_profile(token):
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