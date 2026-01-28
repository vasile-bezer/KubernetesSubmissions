#! /usr/bin/env python3

import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

todos = [
	{"id": 1, "text": "Complete DevOps with Kubernetes chapter 2"},
	{"id": 2, "text": "Complete DevOps with Kubernetes chapter 3"},
	{"id": 3, "text": "Complete DevOps with Kubernetes chapter 4"},
]
next_id = 4

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		
		if self.path == "/todos":
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.send_header("Access-Control-Allow-Origin", "*")
			self.end_headers()
			response = json.dumps(todos)
			self.wfile.write(response.encode('utf-8'))
			return
	
	def do_POST(self):
		global next_id
		
		if self.path == "/todos":
			try:
				content_length = int(self.headers['Content-Length'])
				post_data = self.rfile.read(content_length)
				
				data = json.loads(post_data.decode('utf-8'))
				todo_text = data.get('todo', '').strip()
				
				if not todo_text:
					self.send_response(400)
					self.send_header("Content-Type", "application/json")
					self.send_header("Access-Control-Allow-Origin", "*")
					self.end_headers()
					response = json.dumps({"error": "Todo cannot be empty"})
					self.wfile.write(response.encode('utf-8'))
				elif len(todo_text) > 140:
					self.send_response(400)
					self.send_header("Content-Type", "application/json")
					self.send_header("Access-Control-Allow-Origin", "*")
					self.end_headers()
					response = json.dumps({"error": "Todo must be 140 characters or less"})
					self.wfile.write(response.encode('utf-8'))
				else:
					new_todo = {
						"id": next_id,
						"text": todo_text
					}
					todos.append(new_todo)
					next_id += 1
					
					print(f"Added todo: {todo_text}")
					
					self.send_response(201)
					self.send_header("Content-Type", "application/json")
					self.send_header("Access-Control-Allow-Origin", "*")
					self.end_headers()
					response = json.dumps(new_todo)
					self.wfile.write(response.encode('utf-8'))
			except Exception as e:
				print(f"Error processing POST: {e}")
				self.send_response(500)
				self.send_header("Content-Type", "application/json")
				self.send_header("Access-Control-Allow-Origin", "*")
				self.end_headers()
				response = json.dumps({"error": str(e)})
				self.wfile.write(response.encode('utf-8'))
	
	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()
		return

def main():
	"""main function"""
	
	port = int(os.environ.get("PORT", "3001"))
	
	server = HTTPServer(("0.0.0.0", port), Handler)
	
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