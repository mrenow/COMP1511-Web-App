"""Flask server"""
import sys
from flask_cors import CORS
from flask_mail import Mail
from json import dumps
from flask import Flask, request
from server.AccessError import AccessError
from server.constants import TIMEZONE
from datetime import datetime, tzinfo

APP = Flask(__name__)
CORS(APP)

int_suffixes = ["_id", "start", "end", "length"]


def correct_type(pair):
	key, value = pair
	for suffix in int_suffixes:
		if key.endswith(suffix): 
			return (key, int(value))
	if key.startswith("time_"):
		return (key, datetime.fromtimestamp(int(value), tz = TIMEZONE))
	return (key, value)


def export(route, methods):
	def decorator(function):
		@APP.route(route, methods = methods, endpoint = function.__name__)
		def wrapper():
			try:
				show_request(request)
				request_type_corrected = dict(map(correct_type, request.values.items()))
				response = function(**request_type_corrected)
				show_response(response)
				return response
			except ValueError as err:
				return dict(code = 400,
							name = "ValueError",
							message = f"{function.__name__}: {err}"
				),400
			except AccessError as err:
				return dict(code = 400,
							name = "AccessError",
							message = f"{function.__name__}: {err}"
				),400
		return wrapper
	return decorator

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

if __name__ == '__main__':
	# Generate all routes
	import server.server

	#APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
	APP.run(port = 5001, debug = True)












