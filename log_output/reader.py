#! /usr/bin/env python3

import sys
import os
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		log_file = "/app/logs/output.txt"
		
		content = "Waiting for log file...\n"
		try:
			with open(log_file, "r") as f:
				content = f.read().strip()
			
			ping_pong_count = 0
			with urllib.request.urlopen("http://ping-pong-svc:1234/pings") as response:
				ping_pong_count = response.read().decode('utf-8').strip()
			
			content = f"{content}\nPing / Pongs: {ping_pong_count}\n"
			
		except Exception as e:
			print("Exception:", e)
			content = f"Error reading file: {e}\n"
		
		self.send_response(200)
		self.send_header("Content-Type", "text/plain; charset=utf-8")
		self.end_headers()
		self.wfile.write(content.encode())
	

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