"""Flask server"""
import sys
from flask_cors import CORS
from flask_mail import Mail
from json import dumps
from flask import Flask, request

APP = Flask(__name__)
CORS(APP)


int_prefixes = ["_id", "start", "end", "length"]
int_suffixes = ["time_"]




def correct_type(key, value):
	for prefix in int_prefixes:
		if key.startswith(prefix):
			return (key, int(value))
	for suffix in int_suffixes:
		if key.endswith(suffix): 
			return (key, int(value))
	return (key, value)
	
def export(function, route, methods):
	@APP.route(route, methods = methods)
	def wrapper():
		show_request(request)
		request_type_corrected = dict(map(correct_type, request.values.keys(), request.values.values()))
		response = function(**request_type_corrected)
		show_response(response)
		return response


def show_request(request:Flask.request_class):
	print(
		f"\n{request} \n" + 
		f"\tArgs: {request.args} \n" +  
		f"\tForm: {request.form}\n" 
	)
def show_response(response):
	print(f"Response: {response}\n")

@APP.route('/echo/get', methods=['GET', 'POST'])
def echo1(): 
	""" Description of function """
	response =  dumps({
        'echo' : request.args.get('echo'),
    })
	show_response(response)
	return response

@APP.route('/auth/login', methods = ["POST"])
def auth_login():
	show_request(request)
	response =  s.auth_login(request.values["email"], request.values["password"])
	show_response(response)
	return response


@APP.route("/auth/register", methods = ["POST"])
def auth_register():
	show_request(request)
	response =  s.auth_register(request.values["email"], request.values["password"], request.values["name_first"], request.values["name_last"])
	show_response(response)
	return response

@APP.route("/auth/passwordreset_request", methods = ["POST"])
def auth_passwordreset_request():
	show_request(request)
	response =  s.auth_passwordreset_request(request.values["email"])
	show_response(response)
	return response

@APP.route("/auth/passwordreset_reset", methods = ["POST"])
def auth_passwordreset_reset():
	show_request(request)
	response =  s.auth_passwordreset_reset(request.values["reset_code"], request.values["new_password"])
	show_response(response)
	return response

@APP.route("/channel/invite", methods = ["POST"])
def channel_invite():
	show_request(request)
	response =  s.channel_invite(request.values["token"], int(request.values["channel_id"]), int(request.values["u_id"]))
	show_response(response)
	return response

@APP.route("/channel/details", methods = ["GET"])
def channel_details():
	show_request(request)
	response =  s.channel_details(request.values["token"], int(request.values["channel_id"]))
	show_response(response)
	return response

@APP.route("/channel/messages", methods = ["GET"])
def channel_messages():
	show_request(request)
	response =  s.channel_messages(request.values["token"], int(request.values["channel_id"]), int(request.values["start"]))
	show_response(response)
	return response

@APP.route("/channel/leave", methods = ["POST"])
def channel_leave():
	show_request(request)
	response =  s.channel_leave(request.values["token"], int(request.values["channel_id"]))
	show_response(response)
	return response

@APP.route("/channel/join", methods = ["POST"])
def channel_join():
	show_request(request)
	response =  s.channel_join(request.values["token"], int(request.values["channel_id"]))
	show_response(response)
	return response

@APP.route("/channel/addowner", methods = ["POST"])
def channel_addowner():
	show_request(request)
	response =  s.channel_addowner(request.values["token"], int(request.values["channel_id"]), int(request.values["u_id"]))
	show_response(response)
	return response

@APP.route("/channel/removeowner", methods = ["POST"])
def channel_removeowner():
	show_request(request)
	response =  s.channel_removeowner(request.values["token"], int(request.values["channel_id"]), int(request.values["u_id"]))
	show_response(response)
	return response

@APP.route("/channels/list", methods = ["GET"])
def channels_list():
	show_request(request)
	response =  s.channels_list(request.values["token"])
	show_response(response)
	return response

@APP.route("/channels/listall", methods = ["GET"])
def channels_listall():
	show_request(request)
	response =  s.channels_listall(request.values["token"])
	show_response(response)
	return response

@APP.route("/channels/create", methods = ["POST"])
def channels_create():
	show_request(request)
	response =  s.channels_create(request.values["token"], request.values["name"], request.values["is_public"])
	show_response(response)
	return response

@APP.route("/channels/delete", methods = ["POST"])
def channels_delete():
	show_request(request)
	response =  s.channels_delete(request.values["token"], int(request.values["channel_id"]))
	show_response(response)
	return response

@APP.route("/message/sendlater", methods = ["POST"])
def message_sendlater():
	show_request(request)
	response = s.message_sendlater(request.values["token"], int(request.values["channel_id"]), request.values["message"], int(request.values["time_sent"]))
	show_response(response)
	return response

@APP.route("/message/send", methods = ["POST"])
def message_send():
	show_request(request)
	response =  s.message_send(request.values["token"], int(request.values["channel_id"]), request.values["message"])
	show_response(response)
	return response

@APP.route("/message/remove", methods = ["DELETE"])
def message_remove():
	show_request(request)
	response =  s.message_remove(request.values["token"], int(request.values["message_id"]))
	show_response(response)
	return response

@APP.route("/message/edit", methods = ["PUT"])
def message_edit():
	show_request(request)
	response =  s.message_edit(request.values["token"], int(request.values["message_id"]), request.values["message"])
	show_response(response)
	return response

@APP.route("/message/react", methods = ["POST"])
def message_react():
	show_request(request)
	response =  s.message_react(request.values["token"], int(request.values["message_id"]), int(request.values["react_id"]))
	show_response(response)
	return response

@APP.route("/message/unreact", methods = ["POST"])
def message_unreact():
	show_request(request)
	response =  s.message_unreact(request.values["token"], int(request.values["message_id"]), int(request.values["react_id"]))
	show_response(response)
	return response

@APP.route("/message/pin", methods = ["POST"])
def message_pin():
	show_request(request)
	response =  s.message_pin(request.values["token"], int(request.values["message_id"]))
	show_response(response)
	return response

@APP.route("/message/unpin", methods = ["POST"])
def message_unpin():
	show_request(request)
	response =  s.message_unpin(request.values["token"], int(request.values["message_id"]))
	show_response(response)
	return response

@APP.route("/user/profile", methods = ["GET"])
def user_profile():
	show_request(request)
	response =  s.user_profile(request.values["token"], int(request.values["u_id"]))
	show_response(response)
	return response

@APP.route("/user/profile/setname", methods = ["PUT"])
def user_profile_setname():
	show_request(request)
	response =  s.user_profile_setname(request.values["token"], request.values["name_first"], request.values["name_last"])
	show_response(response)
	return response

@APP.route("/user/profile/setemail", methods = ["PUT"])
def user_profile_setemail():
	show_request(request)
	response =  s.user_profile_setemail(request.values["token"], request.values["email"])
	show_response(response)
	return response

@APP.route("/user/profile/sethandle", methods = ["PUT"])
def user_profile_sethandle():
	show_request(request)
	response =  s.user_profile_sethandle(request.values["token"], request.values["handle_str"])
	show_response(response)
	return response

@APP.route("/user/profiles/uploadphoto", methods = ["POST"])
def user_profiles_uploadphoto():
	show_request(request)
	response =  s.user_profiles_uploadphoto(request.values["token"], request.values["img_url"], request.values["x_start"], request.values["y_start"], request.values["x_end"], request.values["y_end"])
	show_response(response)
	return response

@APP.route("/standup/start", methods = ["POST"])
def standup_start():
	show_request(request)
	response = s.standup_start(request.values["token"], int(request.values["channel_id"]), int(request.values["length"]))
	show_response(response)
	return response

@APP.route("/standup/active", methods = ["GET"])
def standup_active():
	show_request(request)
	response = s.standup_active(request.values["token"], int(request.values["channel_id"]))
	show_response(response)
	return response

@APP.route("/standup/send", methods = ["POST"])
def standup_send():
	show_request(request)
	response =  s.standup_send(request.values["token"], int(request.values["channel_id"]), request.values["message"])
	show_response(response)
	return response


@APP.route("/search", methods = ["GET"])
def search():
	show_request(request)
	response =  s.search(request.values["token"], request.values["query_str"])
	show_response(response)
	return response

@APP.route("/admin/userpermission/change", methods = ["POST"])
def admin_userpermission_change():
	show_request(request)
	response =  s.admin_userpermission_change(request.values["token"], int(request.values["u_id"]), request.values["permission_id"])
	show_response(response)
	return response





if __name__ == '__main__':
    #APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
	APP.run(port = 5001, debug = True)












