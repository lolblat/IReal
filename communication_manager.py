import jwt
import argparse
from queue import Queue
import requests
from threading import Thread

SECRECT_KEY = "RkK1EM4xHRUOfYBXvrw4"
EVENT_QUEUE = Queue()

def pulling(user_token):
	#Pull from the server
	pass

def pass_to_ida():
	#Pass to ida controller.
	pass

def parse_args():
	parser = argparse.ArgumentParser(description="Puller for the IDA Plugin IReal")
	parser.add_argument("token", type=str, description="User token")
	return parser.parse().token

def main(user_token):
	pulling_thread = Thread(target = pulling, args = (user_token, ))
	pulling_thread.start()
	pass_to_ida_thread = Thread(target = pass_to_ida)
	pass_to_ida_thread.start()
	
if __name__ == "__main__":
	user_token = parse_args()
	main(user_token)