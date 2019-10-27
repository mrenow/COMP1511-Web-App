"""Flask server"""
import sys
from flask_cors import CORS
from flask_mail import Mail
from json import dumps
from flask import Flask, request
import server.server as s

APP = Flask(__name__)
CORS(APP)

<<<<<<< HEAD
=======


>>>>>>> fc44c6b6092a9901762cdc432c9b479c725a527c
@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })


@APP.route('/auth/login', methods = ["POST"])
def auth_login():
	return s.auth_login(request.form["email"], request.form["password"])

@APP.route("/auth/logout", methods = ["POST"])
def auth_logout():
	return s.auth_logout(request.form["token"])

@APP.route("/auth/register", methods = ["POST"])
def auth_register():
	return s.auth_register(request.form["email"], request.form["password"], request.form["name_first"], request.form["name_last"])

@APP.route("/auth/passwordreset_request", methods = ["POST"])
def auth_passwordreset_request():
	return s.auth_passwordreset_request(request.form["email"])

@APP.route("/auth/passwordreset_reset", methods = ["POST"])
def auth_passwordreset_reset():
	return s.auth_passwordreset_reset(request.form["reset_code"], request.form["new_password"])

@APP.route("/channel/invite", methods = ["POST"])
def channel_invite():
	return s.channel_invite(request.form["token"], request.form["channel_id"], request.form["u_id"])

@APP.route("/channel/details", methods = ["POST"])
def channel_details():
	return s.channel_details(request.form["token"], request.form["channel_id"])

@APP.route("/channel/messages", methods = ["POST"])
def channel_messages():
	return s.channel_messages(request.form["token"], request.form["channel_id"], request.form["start"])

@APP.route("/channel/leave", methods = ["POST"])
def channel_leave():
	return s.channel_leave(request.form["token"], request.form["channel_id"])

@APP.route("/channel/join", methods = ["POST"])
def channel_join():
	return s.channel_join(request.form["token"], request.form["channel_id"])

@APP.route("/channel/addowner", methods = ["POST"])
def channel_addowner():
	return s.channel_addowner(request.form["token"], request.form["channel_id"], request.form["u_id"])

@APP.route("/channel/removeowner", methods = ["POST"])
def channel_removeowner():
	return s.channel_removeowner(request.form["token"], request.form["channel_id"], request.form["u_id"])

@APP.route("/channels/list", methods = ["POST"])
def channels_list():
	return s.channels_list(request.form["token"])

@APP.route("/channels/listall", methods = ["POST"])
def channels_listall():
	return s.channels_listall(request.form["token"])

@APP.route("/channels/create", methods = ["POST"])
def channels_create():
	return s.channels_create(request.form["token"], request.form["name"], request.form["is_public"])

@APP.route("/channels/delete", methods = ["POST"])
def channels_delete():
	return s.channels_delete(request.form["token"], request.form["channel_id"])

@APP.route("/message/sendlater", methods = ["POST"])
def message_sendlater():
	return s.message_sendlater(request.form["token"], request.form["channel_id"], request.form["message"], request.form["time_sent"])

@APP.route("/message/send", methods = ["POST"])
def message_send():
	return s.message_send(request.form["token"], request.form["channel_id"], request.form["message"])

@APP.route("/message/remove", methods = ["POST"])
def message_remove():
	return s.message_remove(request.form["token"], request.form["message_id"])

@APP.route("/message/edit", methods = ["POST"])
def message_edit():
	return s.message_edit(request.form["token"], request.form["message_id"], request.form["message"])

@APP.route("/message/react", methods = ["POST"])
def message_react():
	return s.message_react(request.form["token"], request.form["message_id"], request.form["react_id"])

@APP.route("/message/unreact", methods = ["POST"])
def message_unreact():
	return s.message_unreact(request.form["token"], request.form["message_id"], request.form["react_id"])

@APP.route("/message/pin", methods = ["POST"])
def message_pin():
	return s.message_pin(request.form["token"], request.form["message_id"])

@APP.route("/message/unpin", methods = ["POST"])
def message_unpin():
	return s.message_unpin(request.form["token"], request.form["message_id"])

@APP.route("/user/profile", methods = ["POST"])
def user_profile():
	return s.user_profile(request.form["token"], request.form["u_id"])

@APP.route("/user/profile_setname", methods = ["POST"])
def user_profile_setname():
	return s.user_profile_setname(request.form["token"], request.form["name_first"], request.form["name_last"])

@APP.route("/user/profile_setemail", methods = ["POST"])
def user_profile_setemail():
	return s.user_profile_setemail(request.form["token"], request.form["email"])

@APP.route("/user/profile_sethandle", methods = ["POST"])
def user_profile_sethandle():
	return s.user_profile_sethandle(request.form["token"], request.form["handle_str"])

@APP.route("/user/profiles_uploadphoto", methods = ["POST"])
def user_profiles_uploadphoto():
	return s.user_profiles_uploadphoto(request.form["token"], request.form["img_url"], request.form["x_start"], request.form["y_start"], request.form["x_end"], request.form["y_end"])

@APP.route("/standup/start", methods = ["POST"])
def standup_start():
	return s.standup_start(request.form["token"], request.form["channel_id"])

@APP.route("/standup/send", methods = ["POST"])
def standup_send():
	return s.standup_send(request.form["token"], request.form["channel_id"], request.form["message"])

@APP.route("/search", methods = ["POST"])
def search():
	return s.search(request.form["token"], request.form["query_str"])

@APP.route("/admin/userpermission/change", methods = ["POST"])
def admin_userpermission_change():
	return s.admin_userpermission_change(request.form["token"], request.form["u_id"], request.form["permission_id"])



if __name__ == '__main__':
    #APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
	APP.run(port = 5513, debug = True)
