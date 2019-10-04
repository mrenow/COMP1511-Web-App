TEST_OWNER_EMAIL = "TODO"
TEST_OWNER_PASSWORD = "TODO"
TEST_EMAIL = "TODO"
TEST_PASSWORD = "TODO"
TEST_INVALID_PASSWORD = TEST_PASSWORD + " "
TEST_INVALID_EMAIL = "TODO"
TEST_INVALID_MESSAGE = "0"*1001
TEST_VALID_MESSAGE = "0"*1000
TEST_VALID_CHANNEL_ID = "TODO"
TEST_INVALID_CHANNEL_ID = "TODO"


def auth_login(email, password):
    pass
def auth_logout(token):
    pass
def auth_register(email, password, name_first, name_last):
    pass
def auth_passwordreset_request(email):
    pass
def auth_passwordreset_reset(reset_code, new_password):
    pass
def channel_invite(token, channel_id, u_id):
    pass
def channel_details(token, channel_id):
    pass
def channel_messages(token, channel_id, start):
    pass
def channel_leave(token, channel_id):
    pass
def channel_join(token, channel_id):
    pass
def channel_addowner(token, channel_id, u_id):
    pass
def channel_removeowner(token, channel_id, u_id):
    pass
def channels_list(token):
    pass
def channels_listall(token):
    pass
def channels_create(token, name, is_public):
    pass
def message_sendlater(token, channel_id, message, time_sent):
    pass
def message_send(token, channel_id, message):
    pass
def message_remove(token, message_id):
    pass
def message_edit(token, message_id, message):
    pass
def message_react(email, password):
    pass
def message_unreact(email, password):
    pass
def message_pin(token, message_id, react_id):
    pass
def message_unpin(token, message_id, react_id):
    pass
def user_profile(token):
    pass
def user_profile_setname(token, name_first, name_last):
    pass
def user_profile_setemail(token, email):
    pass
def user_profile_sethandle(token, handle_str):
    pass
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    pass
def standup_start(token, channel_id):
    pass
def standup_send(token, channel_id, message):
    pass
def search(token, query_str):
    pass
def admin_userpermission_change(token, u_id, permission_id):
    pass