"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request

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


@APP.route("auth/login", match = ["POST"])
def auth_login():
	return server.auth_login(request.form["email"], request.form["password"])

@APP.route("auth/logout", match = ["POST"])
def auth_logout():
	return server.auth_logout(request.form["token"])

@APP.route("auth/register", match = ["POST"])
def auth_register():
	return server.auth_register(request.form["email"], request.form["password"], request.form["name_first"], request.form["name_last"])

@APP.route("auth/passwordreset_request", match = ["POST"])
def auth_passwordreset_request():
	return server.auth_passwordreset_request(request.form["email"])

@APP.route("auth/passwordreset_reset", match = ["POST"])
def auth_passwordreset_reset():
	return server.auth_passwordreset_reset(request.form["reset_code"], request.form["new_password"])

@APP.route("channel/invite", match = ["POST"])
def channel_invite():
	return server.channel_invite(request.form["token"], request.form["channel_id"], request.form["u_id"])

@APP.route("channel/details", match = ["POST"])
def channel_details():
	return server.channel_details(request.form["token"], request.form["channel_id"])

@APP.route("channel/messages", match = ["POST"])
def channel_messages():
	return server.channel_messages(request.form["token"], request.form["channel_id"], request.form["start"])

@APP.route("channel/leave", match = ["POST"])
def channel_leave():
	return server.channel_leave(request.form["token"], request.form["channel_id"])

@APP.route("channel/join", match = ["POST"])
def channel_join():
	return server.channel_join(request.form["token"], request.form["channel_id"])

@APP.route("channel/addowner", match = ["POST"])
def channel_addowner():
	return server.channel_addowner(request.form["token"], request.form["channel_id"], request.form["u_id"])

@APP.route("channel/removeowner", match = ["POST"])
def channel_removeowner():
	return server.channel_removeowner(request.form["token"], request.form["channel_id"], request.form["u_id"])

@APP.route("channels/list", match = ["POST"])
def channels_list():
	return server.channels_list(request.form["token"])

@APP.route("channels/listall", match = ["POST"])
def channels_listall():
	return server.channels_listall(request.form["token"])

@APP.route("channels/create", match = ["POST"])
def channels_create():
	return server.channels_create(request.form["token"], request.form["name"], request.form["is_public"])

@APP.route("channels/delete", match = ["POST"])
def channels_delete():
	return server.channels_delete(request.form["token"], request.form["channel_id"])

@APP.route("message/sendlater", match = ["POST"])
def message_sendlater():
	return server.message_sendlater(request.form["token"], request.form["channel_id"], request.form["message"], request.form["time_sent"])

@APP.route("message/send", match = ["POST"])
def message_send():
	return server.message_send(request.form["token"], request.form["channel_id"], request.form["message"])

@APP.route("message/remove", match = ["POST"])
def message_remove():
	return server.message_remove(request.form["token"], request.form["message_id"])

@APP.route("message/edit", match = ["POST"])
def message_edit():
	return server.message_edit(request.form["token"], request.form["message_id"], request.form["message"])

@APP.route("message/react", match = ["POST"])
def message_react():
	return server.message_react(request.form["token"], request.form["message_id"], request.form["react_id"])

@APP.route("message/unreact", match = ["POST"])
def message_unreact():
	return server.message_unreact(request.form["token"], request.form["message_id"], request.form["react_id"])

@APP.route("message/pin", match = ["POST"])
def message_pin():
	return server.message_pin(request.form["token"], request.form["message_id"])

@APP.route("message/unpin", match = ["POST"])
def message_unpin():
	return server.message_unpin(request.form["token"], request.form["message_id"])

@APP.route("user/profile", match = ["POST"])
def user_profile():
	return server.user_profile(request.form["token"], request.form["u_id"])

@APP.route("user/profile_setname", match = ["POST"])
def user_profile_setname():
	return server.user_profile_setname(request.form["token"], request.form["name_first"], request.form["name_last"])

@APP.route("user/profile_setemail", match = ["POST"])
def user_profile_setemail():
	return server.user_profile_setemail(request.form["token"], request.form["email"])

@APP.route("user/profile_sethandle", match = ["POST"])
def user_profile_sethandle():
	return server.user_profile_sethandle(request.form["token"], request.form["handle_str"])

@APP.route("user/profiles_uploadphoto", match = ["POST"])
def user_profiles_uploadphoto():
	return server.user_profiles_uploadphoto(request.form["token"], request.form["img_url"], request.form["x_start"], request.form["y_start"], request.form["x_end"], request.form["y_end"])

@APP.route("standup/start", match = ["POST"])
def standup_start():
	return server.standup_start(request.form["token"], request.form["channel_id"])

@APP.route("standup/send", match = ["POST"])
def standup_send():
	return server.standup_send(request.form["token"], request.form["channel_id"], request.form["message"])

@APP.route("search", match = ["POST"])
def search(token, query_str):
	return server.search(request.form["token"], request.form["query_str"])

@APP.route("admin/userpermission/change", match = ["POST"])
def admin_userpermission_change():
	return server.admin_userpermission_change(request.form["token"], request.form["u_id"], request.form["permission_id"])



if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

