from server.server import *
from server.AccessError import AccessError
import pytest

permissions = ["owner", "admin", "member"]


@pytest.fixture
def clear():
    reset()


def test_admin_userpermission_change(clear):
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]
    
    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    with pytest.raises(AccessError):
        admin_userpermission_change(token2, userID, ADMIN)
    with pytest.raises(ValueError):
        admin_userpermission_change(token, userID2, 123456)
    with pytest.raises(ValueError):
        admin_userpermission_change(token, 123456, MEMBER)

    admin_userpermission_change(token, userID2, ADMIN)
    channel_1 = channels_create(token2, "channel1", True)

    admin_userpermission_change(token, userID2, MEMBER)
    with pytest.raises(AccessError):
        channel_1 = channels_create(token2, "channel1", True)


#parts of channel_detail tested
def test_channels_create_and_list_all(clear):
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    #check if channel is listed after creation
    channel_1 = channels_create(token, "channel1", True)
    lst = channels_listall(token)
    assert lst["channels"][0]["name"] == "channel1"
    assert lst["channels"][0]["id"] == channel_1

    #check if channel name shown in channel details
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["name"][0] == "channel1"
    
    #check if channel is listed after creation
    channel_2 = channels_create(token, "channel2", True)
    lst = channels_listall(token)
    assert lst["channels"][0]["name"] == "channel1"
    assert lst["channels"][0]["id"] == channel_1
    assert lst["channels"][1]["name"] == "channel2"
    assert lst["channels"][1]["id"] == channel_2

    #check if channel name shown in channel details
    channel2_details = channel_details(token, channel_2)
    assert channel2_details["name"][1] == "channel2"

    #check if ValueError raised if name is over 20 characters
    with pytest.raises(ValueError):
        channel_3 = channels_create(token, "channelfdahfldkajdfhlakdjfhalkdjfhlajdf", True)

    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    #check whcih error is raised when two parameters are wrong
    with pytest.raises(ValueError):
        channel_3 = channels_create(token2, "channelfdahfldkajdfhlakdjfhalkdjfhlajdf", True)
    with pytest.raises(AccessError):
        channel_3 = channels_create(token2, "channelf2", True)
    
#parts of channel_detail tested
def test_channel_join(clear):
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    channel_1 = channels_create(token, "channel1", True)
    channel_2 = channels_create(token, "channel2", False)

    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    #check if second user listed in channel member after channel_join
    channel_join(token2, channel_1)
    channel1_details = channel_details(token2, channel_1)
    assert channel1_details["all_members"][0]["u_id"] == userID
    assert channel1_details["all_members"][1]["u_id"] == userID2

    #check if AccessError raised when attempting to join private channel
    with pytest.raises(AccessError):
        channel_join(token2, channel_2)
    channel2_details = channel_details(token, channel_2)
    assert len(channel2_details["allmembers"]) == 1

    #check if ValueError raised when given unknown channel ID
    with pytest.raises(ValueError):
        channel_join(token2, 123456)

def test_channel_leave(clear):
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    channel_1 = channels_create(token, "channel1", True)

    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    #checks if user 2 successfully joins
    channel_join(token2, channel_1)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["all_members"][0]["u_id"] == userID
    assert channel1_details["all_members"][1]["u_id"] == userID2

    #checks if user successfully left
    channel_leave(token2, channel_1)
    channel1_details = channel_details(token, channel_1)
    assert len(channel1_details["allmembers"]) == 1
    assert channel1_details["all_members"][0]["u_id"] == userID

def test_channel_invite(clear):
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    channel_1 = channels_create(token, "channel1", False)

    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    login3 = auth_register("jason@gmail.com", "dafadkh;lktlk444", "Jason", "Xing")
    userID3 = login3["u_id"]
    token3 = login3["token"]

    #checks if ValueError raised if non-member attempts to invite
    with pytest.raises(ValueError):
        channel_invite(token2, channel_1, userID3)
    #checks if invite successful
    channel_invite(token, channel_1, userID2)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["all_members"][0]["u_id"] == userID
    assert channel1_details["all_members"][1]["u_id"] == userID2

    #checks if user2, now a member can invite user3
    channel_invite(token2, channel_1, userID3)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["all_members"][0]["u_id"] == userID
    assert channel1_details["all_members"][1]["u_id"] == userID2
    assert channel1_details["all_members"][2]["u_id"] == userID3

    #checks if ValueError if channel_id unknown
    with pytest.raises(ValueError):
        channel_join(token2, channel_1)



def test_channels_list(clear):
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    channel_1 = channels_create(token, "channel1", True)
    lst = channels_list(token)
    assert lst["channels"][0]["id"] == channel_1

    #check if creator of channel_1 and channel_2 is part of two channels
    channel_2 = channels_create(token, "channel2", True)
    lst = channels_list(token)
    assert lst["channels"][0]["id"] == channel_1
    assert lst["channels"][1]["id"] == channel_2

    #check if channel_1 is listed for user2 after join
    channel_join(token2, channel_1)
    lst = channels_list(token2)
    assert lst["channels"][0]["id"] == channel_1

    #check if channel_2 is listed fo ruser2 after invite
    channel_invite(token, channel_2, userID2)
    lst = channels_list(token2)
    assert lst["channels"][0]["id"] == channel_1
    assert lst["channels"][1]["id"] == channel_2







#parts of channel_detail tested
def test_channel_addowner(clear):

    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    #check if server owner/channel creator is listed as channel owner
    channel_1 = channels_create (token, "channel1", True)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["owner_members"][0]["u_id"] == userID

    #check if adding channel owner as channel owner raises ValueError
    with pytest.raises(ValueError):
        channel_addowner(token,channel_1, userID) 


    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    #checks if unauthorized members can add owners
    with pytest.raises(AccessError):
        channel_addowner(token2,channel_1, userID2)
    with pytest.raises(AccessError):
        channel_addowner(token2,channel_1, userID)

    #checks if second channel owner successfully adds by checking channel owner list
    channel_addowner(token,channel_1, userID2)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["owner_members"][1]["u_id"] == userID2
    

    #check if second channel owner successfully adds by adding again and see if ValueError is raised
    with pytest.raises(ValueError):
        channel_addowner(token,channel_1, userID2)
    

    login3 = auth_register("jason@gmail.com", "dafadkh;lktlk444", "Jason", "Xing")
    userID3 = login3["u_id"]
    token3 = login3["token"]

    #check if ValueError is raised when channel id is unknown
    with pytest.raises(ValueError):
         channel_addowner(token,-1, userID3)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["owner_members"][1]["u_id"] == userID2
    

    #check if second channel owner successfully adds by adding again and see if ValueError is raised
    with pytest.raises(ValueError):
        channel_addowner(token,channel_1, userID2)
    

    login3 = auth_register("jason@gmail.com", "dafadkh;lktlk444", "Jason", "Xing")
    userID3 = login3["u_id"]
    token3 = login3["token"]

    #check if ValueError is raised when channel id is unknown
    channels_delete(token, channel_1)
    with pytest.raises(ValueError):
         channel_addowner(token,channel_1, userID3)   

def test_channel_removeowner(clear):
    login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
    userID = login["u_id"]
    token = login["token"]

    #check if server owner/channel creator is listed as channel owner
    channel_1 = channels_create (token, "channel1", True)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["owner_members"][0]["u_id"] == userID
    login2 = auth_register("ezra@gmail.com", "dlfajhldkhf1111", "Ezra", "Hui")
    userID2 = login2["u_id"]
    token2 = login2["token"]

    #checks if ValueError is raised when non-owner is removed
    with pytest.raises(ValueError):
        channel_removeowner(token, channel_1, userID2)
    
    #checks if AccessError is raised when non-owner tries to remove
    with pytest.raises(AccessError):
        channel_removeowner(token2, channel_1, userID)

    #checks if second channel owner successfully adds by checking channel owner list
    channel_addowner(token,channel_1, userID2)
    channel1_details = channel_details(token, channel_1)
    assert channel1_details["owner_members"][1]["u_id"] == userID2
    assert len(channel1_details["owner_members"]) == 2

    #checks if remove owner works now
    channel_removeowner(token2, channel_1, userID)
    channel1_details = channel_details(token2, channel_1)
    assert len(channel1_details["owner_members"]) == 1

    #check if ValueError is raised when channel id is unknown
    with pytest.raises(ValueError):
         channel_removeowner(token, -1, userID)






    
    


