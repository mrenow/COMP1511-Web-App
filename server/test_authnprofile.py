import time
import pytest

from server.AccessError import AccessError
from server.server import *


@pytest.fixture
def clear():
	reset()


def test_auth_login(clear):
	# Set up
	userId1, token1 = auth_register("good@email.com", "123456", "jason", "xing")
	userId2, token2 = auth_register("good1@email.com", "654321", "jason", "xing")
	# Bad email
	with pytest.raises(ValueError):
		userId1, token1 = auth_login("bademail.com", "123456")
	# Not registered
	with pytest.raises(ValueError):
		userId3, token3 = auth_login("good2@email.com", "123456")
	# Wrong Password
	with pytest.raises(ValueError):
		userId2, token2 = auth_login("good1@email.com", "654321X")

def test_auth_logout(clear):
	# See user profile section
    pass

def test_auth_register(clear):
	# Edge Case
    userId, token = auth_register("good@email.com", "123456", "0"*50, "0"*50)
	# Bad email 
    with pytest.raises(ValueError):
        userId1, token1 = auth_register("bademail.com", "123456", "jason", "xing")
	# Bad password 
    with pytest.raises(ValueError):
        userId2, token2 = auth_register("good1@email.com", "nopw", "jason", "xing")
	# Bad first name
    with pytest.raises(ValueError):
        userId3, token3 = auth_register("good1@email.com", "123456", "0"*51, "xing")
	# Bad last name 
    with pytest.raises(ValueError):
        userId4, token4 = auth_register("good1@email.com", "123456", "jason","0"*51)
	# Email in use
    with pytest.raises(ValueError):
        userId6, token6 = auth_register("good@email.com", "123456", "jason", "xing")
        

def test_auth_passwordreset_request(clear):
	# Set up
    userId1, token1 = auth_register("good@email.com", "123456", "jason", "xing")
	# Can't access email so no tests
def test_auth_passwordreset_reset():
    # Set up
	userId1, token1 = auth_register("good10@email.com", "123456", "jason", "xing")
	# Test if new password is valid
	with pytest.raises(ValueError):
		auth_passwordreset_reset("123456", "123X")

def test_user_profile(clear):
	# Set up
	login1 = auth_register("good1@email.com", "123456", "jason", "xing")
	userId1 = login1["u_id"]
	token1 = login1["token"]
	login2 = auth_login("good1@email.com", "123456")
	userId2 = login2["u_id"]
	token2 = login2["token"]
	# Not a valid user
	with pytest.raises(ValueError):
		user_profile(token1, -1)
	# Check token is invalid (login token)
	auth_logout(token2)
	with pytest.raises(ValueError):
		user_profile(token2, userId2)
	user_profile(token1, userId1)

def test_user_profile_setname(clear):
    # Set up
	login1 = auth_register("good1@email.com", "123456", "jason", "xing")
	userId1 = login1["u_id"]
	token1 = login1["token"]
	login2 = auth_register("good2@email.com", "123456", "jason", "xing")
	userId2 = login2["u_id"]
	token2 = login2["token"]
	# Invalid first name
	with pytest.raises(ValueError):
		user_profile_setname(token1, "0"*51, "xing")
	# Invalid last name
	with pytest.raises(ValueError):
		user_profile_setname(token1, "jason", "0"*51)
	# Check token is invalid (register token)
	auth_logout(token1)
	with pytest.raises(ValueError):
		user_profile_setname(token1, "jason", "xing")
	
def test_user_profile_setemail(clear):
    # Set up
	login1 = auth_register("good1@email.com", "123456", "jason", "xing")
	userId1 = login1["u_id"]
	token1 = login1["token"]
	login2 = auth_register("good2@email.com", "123456", "jason", "xing")
	userId2 = login2["u_id"]
	token2 = login2["token"]
	login3 = auth_register("good3@email.com", "123456", "jason", "xing")
	userId3 = login3["u_id"]
	token3 = login3["token"]
	# Email not valid
	with pytest.raises(ValueError):
		user_profile_setemail(token1, "bademail.com")
	# Email in use
	with pytest.raises(ValueError):
		user_profile_setemail(token1, "good2@email.com")
	# Check token is invalid (login token)
	auth_logout(token3)
	with pytest.raises(ValueError):
		user_profile_setname(token3, "jasonxing@email.com", "Jyden")
	
def test_user_profile_sethandle(clear):
    # Set up
	login = auth_register("albertyeh199909@gmail.com", "fksafkljfg1111", "Albert", "Yeh")
	userId1 = login["u_id"]
	token1 = login["token"]
	
	# Edge case
	user_profile_sethandle(token1, "0"*20)
	# Handle is too long
	with pytest.raises(ValueError):
		user_profile_sethandle(token1, "0"*21)
	# Check token is valid (register token)
	auth_logout(token1)
	with pytest.raises(ValueError):
		user_profile_sethandle(token1, "jason")

def test_user_profiles_uploadphoto(clear):
    # Set up
	login = auth_register("good1@email.com", "123456", "jason", "xing")
	userId1 = login["u_id"]
	token1 = login["token"]
	login = auth_login("good1@email.com", "123456")
	userId2 = login["u_id"]
	token2 = login["token"]
	# HTTP status other than 200
	# Probably untestable at this point

	# x and y values are too big
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, "https://assets.pernod-ricard.com/nz/media_images/test.jpg?hUV74FvXQrWUBk1P2.fBvzoBUmjZ1wct", 0 , 0, 700, 700)
	# Check token is valid (login token)
	auth_logout(token2)
	with pytest.raises(AccessError):
		user_profiles_uploadphoto(token2, "https://assets.pernod-ricard.com/nz/media_images/test.jpg?hUV74FvXQrWUBk1P2.fBvzoBUmjZ1wct", 0 , 0, 600, 600)