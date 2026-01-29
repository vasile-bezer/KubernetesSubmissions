#!/usr/bin/env python3

import sys
import os
import json
import urllib.request
import urllib.error

def get_random_wikipedia_url():
    """
    Fetch a random Wikipedia article URL by following the redirect
    from https://en.wikipedia.org/wiki/Special:Random
    """
    try:
        req = urllib.request.Request(
            'https://en.wikipedia.org/wiki/Special:Random',
            headers={'User-Agent': 'Wikipedia-Todo-Bot/1.0'}
        )
        
        # Don't follow redirects automatically, we want to get the Location header
        with urllib.request.urlopen(req, timeout=10) as response:
            # If we get here, it means the URL was followed
            # The final URL is in response.url
            return response.url
            
    except urllib.error.HTTPError as e:
        # Sometimes we might get a redirect response
        if 'Location' in e.headers:
            return e.headers['Location']
        raise
    except Exception as e:
        print(f"Error getting random Wikipedia URL: {e}")
        raise


def add_todo_to_backend(todo_text):
    """
    POST a new todo to the backend service
    """
    backend_url = os.environ.get("BACKEND_URL", "http://todo-backend-svc.project.svc.cluster.local:3001/todos")
    
    try:
        data = json.dumps({"todo": todo_text}).encode('utf-8')
        
        req = urllib.request.Request(
            backend_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Successfully added todo: {result}")
            return result
            
    except Exception as e:
        print(f"Error adding todo to backend: {e}")
        raise


def main():
    """Main function"""
    try:
        # Get random Wikipedia URL
        print("Fetching random Wikipedia article...", flush=True)
        wikipedia_url = get_random_wikipedia_url()
        print(f"Got URL: {wikipedia_url}", flush=True)
        
        # Create todo text
        todo_text = f"Read {wikipedia_url}"
        print(f"Creating todo: {todo_text}", flush=True)
        
        # Add to backend
        add_todo_to_backend(todo_text)
        
        print("✓ Successfully created Wikipedia todo!", flush=True)
        return 0
        
    except Exception as e:
        print(f"✗ Failed to create todo: {e}", flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
