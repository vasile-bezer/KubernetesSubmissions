#! /usr/bin/env python3

import time
import sys
import os
import uuid
import datetime


def generate_random_string():
	"""Generate a random uuid"""
	return uuid.uuid4()


def main():
	"""main function"""
	
	random_uuid = generate_random_string()
	datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
	log_file = "/app/logs/output.txt"
	
	os.makedirs(os.path.dirname(log_file), exist_ok=True)
	
	while True:
		datetime_now = datetime.datetime.now().strftime(datetime_format)
		log_line = f"{datetime_now}: {random_uuid}\n"
		
		with open(log_file, 'w') as f:
			f.write(log_line)
		
		print(log_line.strip())
		
		time.sleep(5)


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