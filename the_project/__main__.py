#! /usr/bin/env python3

import sys
import os
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64


image_file = "/app/cache/current_image.jpg"
last_download_time = 0

todos = [
	"Complete DevOps with Kubernetes chapter 2",
	"Complete DevOps with Kubernetes chapter 3",
	"Complete DevOps with Kubernetes chapter 4",
]


def download_new_image():
	"""download a image"""
	global last_download_time
	
	try:
		os.makedirs(os.path.dirname(image_file), exist_ok=True)
		
		url_with_random = f"https://picsum.photos/1200?random={int(time.time())}"
		print(f"Downloading new image from {url_with_random}")
		
		with urllib.request.urlopen(url_with_random, timeout=10) as response:
			image_data = response.read()
		
		with open(image_file, 'wb') as f:
			f.write(image_data)
		
		last_download_time = time.time()
		
		return image_data
	except Exception as e:
		print(f"Error downloading image: {e}")
		return None


def get_image():
	"""get current image"""
	global last_download_time
	
	os.makedirs(os.path.dirname(image_file), exist_ok=True)
	
	age = time.time() - last_download_time if last_download_time > 0 else float('inf')
	
	if age > 10 * 60:
		print(f"Cache expired (age: {age:.1f}s), downloading new image")
		new_image = download_new_image()
		if new_image:
			return new_image
	
	try:
		if os.path.exists(image_file):
			print(f"Serving cached image (age: {age:.1f}s)")
			with open(image_file, 'rb') as f:
				return f.read()
	except Exception as e:
		print(f"Error reading cached image: {e}")
	
	return download_new_image()


class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		
		image_base64 = base64.b64encode(get_image()).decode('utf-8')
		
		todos_html = ""
		for todo in todos:
			todos_html += f"<li>{todo}</li>\n"
		
		html_content = f"""<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>The Project App</title>
	</head>
	<body>
		<div class="container">
			<h1>The project App</h1>
			<img src="data:image/jpeg;base64,{image_base64}" alt="Random Image">
			
			<div class="todo-section">
				<h2>Todos</h2>
				<div class="todo-input-container">
					<input 
						type="text" 
						id="todo-input" 
						maxlength="140"
					>
					<button id="create-todo">Create todo</button>
				</div>
				
				<ul id="todo-list">
					{todos_html}
				</ul>
			</div>
			
			<footer>DevOps with Kubernetes 2025</footer>
		</div>
		
		<script>
			const todoInput = document.getElementById('todo-input');
			const sendButton = document.getElementById('create-todo');
			const charCount = document.getElementById('char-count');
			const charCounter = document.querySelector('.char-counter');
			const todoList = document.getElementById('todo-list');
			
			todoInput.addEventListener('input', function() {{
				const length = this.value.length;
				charCount.textContent = length;
				
				if (length > 140) {{
					charCounter.classList.add('error');
					sendButton.disabled = true;
				}} else {{
					charCounter.classList.remove('error');
					sendButton.disabled = length === 0;
				}}
			}});
			
			sendButton.addEventListener('click', function() {{
				const todo = todoInput.value.trim();
				if (todo && todo.length <= 140) {{
					const li = document.createElement('li');
					li.textContent = todo;
					todoList.appendChild(li);
					
					todoInput.value = '';
					charCount.textContent = '0';
					sendButton.disabled = true;
				}}
			}});
		</script>
	</body>
</html>"""
			
		self.send_response(200)
		self.send_header("Content-Type", "text/html; charset=utf-8")
		self.end_headers()
		self.wfile.write(html_content.encode('utf-8'))
		return


def main():
	"""main function"""
	
	port = int(os.environ.get("PORT", "3000"))
	
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