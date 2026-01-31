#! /usr/bin/env python3

import sys
import os
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler


def get_db_connection():
	return psycopg2.connect(
		host=os.environ.get("POSTGRES_HOST", "postgres-svc.exercises.svc.cluster.local"),
		database=os.environ.get("POSTGRES_DB", "pingpong"),
		user=os.environ.get("POSTGRES_USER", "postgres"),
		password=os.environ.get("POSTGRES_PASSWORD", "postgres")
	)


def get_counter():
	try:
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute("SELECT value FROM counter WHERE id = 1")
		result = cur.fetchone()
		cur.close()
		conn.close()
		return result[0] if result else 0
	except Exception as e:
		print(f"Error getting counter: {e}")
		return 0


def increment_counter():
	try:
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute("UPDATE counter SET value = value + 1 WHERE id = 1 RETURNING value")
		result = cur.fetchone()
		conn.commit()
		cur.close()
		conn.close()
		return result[0] if result else 0
	except Exception as e:
		print(f"Error incrementing counter: {e}")
		return 0


class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		
		# Main endpoint - increment and return pong
		if self.path == "/":
			counter = increment_counter()
			self.send_response(200)
			self.send_header("Content-Type", "text/plain; charset=utf-8")
			self.end_headers()
			answer = f"pong {counter}\n"
			self.wfile.write(answer.encode("utf-8"))
			return
		
		# Endpoint to just get the counter value without incrementing
		if self.path == "/pings":
			counter = get_counter()
			self.send_response(200)
			self.send_header("Content-Type", "text/plain; charset=utf-8")
			self.end_headers()
			self.wfile.write(str(counter).encode("utf-8"))
			return
		
		# Default 404
		self.send_response(404)
		self.send_header("Content-Type", "text/plain; charset=utf-8")
		self.end_headers()
		self.wfile.write(b"Not Found\n")
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