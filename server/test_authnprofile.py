import time
import pytest

from AccessError import AccessError
from server import *

def test_auth_login():

#   userId, token = auth_login("goodemail@123.com", 12345)
#  ass
def test_auth_logout():
    pass
def test_auth_register():
    userId , token = auth_register("good@email.com", "12345", "jason", "xing")
    with pytest.raises(ValueError):
        userId1, token1 = auth_register("bademail.com", "12345", "jason", "xing")
        userId2, token2 = auth_register("good@email.com", "bad", "jason", "xing")
        userId3, token3 = auth_register("good@email.com", "12345", "0"*51, "xing")
        userId4, token4 = auth_register("good@email.com", "12345", "jason","0"*51)
        userId5, token5 = auth_register("good@email.com", "12345", "0"*50, "0"*50)
        userId6, token6 = auth_register("good@email.com", "12345", "jason", "xing")
        

def test_auth_passwordreset_request():
    pass
def test_auth_passwordreset_reset():
    pass
def test_user_profile():
    pass
def test_user_profile_setname():
    pass
def test_user_profile_setemail():
    pass
def test_user_profile_sethandle():
    pass
def test_user_profiles_uploadphoto():
    pass