import pytest
from server.server import *

def invalid_token_test():
    user = auth_login(TEST_EMAIL, TEST_PASSWORD)
    auth_logout(user)
    with pytest.raises(ValueError):
        message(user, TEST_VALID_CHANNEL_ID)