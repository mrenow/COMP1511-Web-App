from server.server import *
import pytest

def last_message(token, channel_id):
    return channel_messages(token, channel_id, start = 0)[0];


def send_test():
    usertok = auth_login(TEST_EMAIL, TEST_PASSWORD)
    message_send(usertok, TEST_VALID_CHANNEL_ID, "testing")
    message_send(usertok, TEST_VALID_CHANNEL_ID, "one")
    message_send(usertok, TEST_VALID_CHANNEL_ID, "two")
    message_send(usertok, TEST_VALID_CHANNEL_ID, "three")
    expected_messages = [
        {}


    ]

    assert channel_messages(usertok, TEST_VALID_CHANNEL_ID, start = 0) == {}




def remove_test():

    pass

def edit_test():
    pass
    with pytest.rais1

send_test()



