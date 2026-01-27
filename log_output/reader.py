#! /usr/bin/env python3

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		log_file = "/app/logs/output.txt"
		counter_file = "/app/data/pingpong_counter.txt"
		
		content = "Waiting for log file...\n"
		try:
			with open(log_file, "r") as f:
				content = f.read().strip()
			
			ping_pong_count = 0
			if os.path.exists(counter_file):
				with open(counter_file, "r") as f:
					ping_pong_count = f.read().strip()
			
			content = f"{content}\nPing / Pongs: {ping_pong_count}\n"
			
		except Exception as e:
			print("Exception:", e)
			content = f"Error reading file: {e}\n"
		
		self.send_response(200)
		self.send_header("Content-Type", "text/plain; charset=utf-8")
		self.end_headers()
		self.wfile.write(content.encode())
	
	def log_message(self, format, *args):
		# Suppress HTTP request logs
		pass

def main():
	"""main function"""
	
	port = int(os.environ.get("PORT", "3000"))
	
	server = HTTPServer(("0.0.0.0", port), Handler)
	
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		server.server_close()

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