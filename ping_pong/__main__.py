#! /usr/bin/env python3

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

counter = 0
counter_file = "/app/data/pingpong_counter.txt"


def write_counter(value):
	try:
		os.makedirs(os.path.dirname(counter_file), exist_ok=True)
		with open(counter_file, 'w') as f:
			f.write(str(value))
	except Exception as e:
		print(f"Error writing file: {e}")


class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		global counter
		self.send_response(200)
		self.send_header("Content-Type", "text/plain; charset=utf-8")
		self.end_headers()
		answer = f"pong {counter}\n"
		self.wfile.write(answer.encode("utf-8"))
		counter += 1
		write_counter(counter)
		return


def main():
	"""Start the ping-pong HTTP server"""
	
	port = int(os.environ.get("PORT", "3000"))
	
	server = HTTPServer(("0.0.0.0", port), Handler)
	
	# Required startup message
	print(f"Server started in port {port}")
	
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		server.server_close()
	
	return 0


def init():
	"""Handle main init"""
	
	if sys.version_info < (3, 9):
		sys.exit(
			"{0} requires Python version 3.9 or higher...\nyou are trying to run with Python version {1}...\nexiting...".format(
				os.path.basename(__file__), platform.python_version()
			)
		)

	if __name__ == "__main__":
		sys.exit(main())


init()