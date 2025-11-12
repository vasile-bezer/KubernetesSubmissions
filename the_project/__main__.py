#! /usr/bin/env python3

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/":
			self.send_response(200)
			self.send_header("Content-Type", "text/plain; charset=utf-8")
			self.end_headers()
			self.wfile.write(b"ok")
			return

		# Simple placeholder for the todo app root
		self.send_response(200)
		self.send_header("Content-Type", "text/plain; charset=utf-8")
		self.end_headers()
		self.wfile.write(b"Todo app placeholder")


def main():
	"""Start the todo-app HTTP server"""
	
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