#! /usr/bin/env python3

import sys
import os
import json
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler


def get_db_connection():
	return psycopg2.connect(
		host=os.environ.get("POSTGRES_HOST", "todo-db-svc.project.svc.cluster.local"),
		database=os.environ.get("POSTGRES_DB", "tododb"),
		user=os.environ.get("POSTGRES_USER", "todouser"),
		password=os.environ.get("POSTGRES_PASSWORD", "todopassword")
	)


def get_todos():
	try:
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute("SELECT id, text FROM todos ORDER BY id")
		rows = cur.fetchall()
		cur.close()
		conn.close()
		return [{"id": row[0], "text": row[1]} for row in rows]
	except Exception as e:
		print(f"Error getting todos: {e}")
		return []


def add_todo(text):
	try:
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute("INSERT INTO todos (text) VALUES (%s) RETURNING id, text", (text,))
		row = cur.fetchone()
		conn.commit()
		cur.close()
		conn.close()
		return {"id": row[0], "text": row[1]} if row else None
	except Exception as e:
		print(f"Error adding todo: {e}")
		return None


class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		
		if self.path == "/todos":
			todos = get_todos()
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.send_header("Access-Control-Allow-Origin", "*")
			self.end_headers()
			response = json.dumps(todos)
			self.wfile.write(response.encode('utf-8'))
			return
	
	def do_POST(self):
		
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
					new_todo = add_todo(todo_text)
					
					if new_todo:
						print(f"Added todo: {todo_text}")
						
						self.send_response(201)
						self.send_header("Content-Type", "application/json")
						self.send_header("Access-Control-Allow-Origin", "*")
						self.end_headers()
						response = json.dumps(new_todo)
						self.wfile.write(response.encode('utf-8'))
					else:
						self.send_response(500)
						self.send_header("Content-Type", "application/json")
						self.send_header("Access-Control-Allow-Origin", "*")
						self.end_headers()
						response = json.dumps({"error": "Failed to add todo"})
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