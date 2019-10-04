from server import *
'''
TEST_OWNER_EMAIL = "TODO"
TEST_OWNER_PASSWORD = "TODO"
TEST_EMAIL = "TODO"
TEST_PASSWORD = "TODO"
TEST_INVALID_PASSWORD = TEST_PASSWORD + " "
TEST_INVALID_EMAIL = "TODO"
TEST_INVALID_MESSAGE = "0"*1001
TEST_VALID_MESSAGE = "0"*1000
TEST_VALID_CHANNEL = "TODO"
TEST_INVALID_CHANNEL = "TODO"

def channel_addowner(token, channel_id, u_id):
    pass
def channel_removeowner(token, channel_id, u_id):
    pass
def admin_userpermission_change(token, u_id, permission_id):
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
def search(token, query_str):
    pass
'''
def test_channel_addowner():
    login = auth_login(TEST_EMAIL,TEST_PASSWORD)
    userID,token = login
    TEST
    assert 