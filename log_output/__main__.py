#! /usr/bin/env python3

import time
import sys
import os
import uuid
import datetime
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


random_uuid, datetime_format = None, "%Y-%m-%dT%H:%M:%S.%fZ"

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		global random_uuid
		self.send_response(200)
		self.send_header("Content-Type", "text/plain; charset=utf-8")
		self.end_headers()
		answer = f"{datetime.datetime.now().strftime(datetime_format)}: {random_uuid}"
		self.wfile.write(answer.encode())
		return
	
def generate_random_string():
	"""generate a random uuid and print it with a timestamp"""
	
	return uuid.uuid4()


def main():
	"""main function"""
	global random_uuid
	random_uuid = generate_random_string()

	port = int(os.environ.get("PORT", "3000"))
	server = HTTPServer(("0.0.0.0", port), Handler)

	# Start HTTP server in background thread
	server_thread = threading.Thread(target=server.serve_forever, daemon=True)
	server_thread.start()

	# Log to stdout every 5 seconds
	while True:
		datetime_now = datetime.datetime.now().strftime(datetime_format)
		print(f"{datetime_now}: {random_uuid}")
		time.sleep(5)
	
	return 0


def init():
	"""Handle main init"""
	#if "linux" not in sys.platform:
	#	sys.exit(
	#		"{0} only works on Linux... exiting...".format(os.path.basename(__file__))
	#	)

	if sys.version_info < (3, 9):
		sys.exit(
			"{0} requires Python version 3.9 or higher...\nyou are trying to run with Python version {1}...\nexiting...".format(
				os.path.basename(__file__), platform.python_version()
			)
		)

	if __name__ == "__main__":
		sys.exit(main())


init()