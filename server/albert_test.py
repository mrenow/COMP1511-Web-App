from server import *
from AccessError import AccessError
'''

//def channel_addowner(token, channel_id, u_id):
    pass
def channel_removeowner(token, channel_id, u_id):
    pass
def admin_userpermission_change(token, u_id, permission_id):
    pass
def channel_invite(token, channel_id, u_id):
    pass
def channel_details(token, channel_id):
    pass
def channel_leave(token, channel_id):
    pass
def channel_join(token, channel_id):
    pass
def channels_list(token):
    pass
//def channels_listall(token):
    pass
//def channels_create(token, name, is_public):
def search(token, query_str):
    pass
'''
def test_channel_create_and_list_all():
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    channel_1 = channels_create(token, "channel1", True)
    lst = channels_listall(token)
    assert lst["channels"][0]["name"] == "channel1"
    assert lst["channels"][0]["id"] == channel_1
    
    channel_2 = channels_create(token, "channel2", True)
    lst = channels_listall(token)
    assert lst["channels"][0]["name"] == "channel1"
    assert lst["channels"][0]["id"] == channel_1
    assert lst["channels"][1]["name"] == "channel2"
    assert lst["channels"][1]["id"] == channel_2

    with pytest.raise(ValueError):
        channel_3 = channels_create(token, channelfdahfldkajdfhlakdjfhalkdjfhlajdf, True)

    auth_logout(token)
    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    with pytest.raise(AccessError):
        channel_3 = channels_create(token2, channelfdahfldkajdfhlakdjfhalkdjfhlajdf, True)








def test_channel_addowner():

    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    #check if server owner/channel creator is listed as channel owner
    channel_1 = channels_create (token, "channel1", True)
    channel1_details = channel1_details(token, channel_1)
    assert channel1_details["owner_members"][0]["u_id"] == userID

    #check if adding channel owner as channel owner raises ValueError
    with pytest.raises(ValueError):
        channel_addowner(token,channel_1, userID) 

    auth_logout(token)
    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    #checks if unauthorized members can add owners
    with pytest.raises(AccessError):
        channel_addowner(token2,channel_1, userID2)
    with pytest.raises(AccessError):
        channel_addowner(token2,channel_1, userID)

    auth_logout(token)
    login = auth_login("albertyeh199909@gmail.com", "fksafkljfg1111")
    userID = login["u_id"]
    token = login["token"]

    #checks if second channel owner successfully adds by checking channel owner list
    channel_addowner(token,channel_1, userID2)
    channel1_details = channel1_details(token, channel_1)
    assert channel1_details["owner_members"][1]["u_id"] == userID2

    #check if second channel owner successfully adds by adding again and see if ValueError is raised
    with pytest.raises(ValueError):
        channel_addowner(token,channel_1, userID2)
    
    auth_logout(token)
    login3 = auth_register("jason@gmail.com", "dafadkh;lktlk444", "Jason", "Xing")
    userID3 = login3["u_id"]
    token3 = login3["token"]

    login = auth_login("albertyeh199909@gmail.com", "fksafkljfg1111")
    userID = login["u_id"]
    token = login["token"]

    #check if ValueError is raised when channel id is unknown
    channels_delete(token, channel_1)
    with pytest.raises(ValueError):
         channel_addowner(token,channel_1, userID3)   







    
    


