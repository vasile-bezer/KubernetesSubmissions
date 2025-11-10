#! /usr/bin/env python3

import time
import sys
import os
import uuid
import datetime


def generate_random_string():
	"""generate a random uuid and print it with a timestamp"""
	
	return uuid.uuid4()


def main():
	"""main function"""
	
	random_uuid = generate_random_string()
	datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

	while True:
		datetime_now = datetime.datetime.now().strftime(datetime_format)
		print(f"{datetime_now}: {random_uuid}")
		time.sleep(5)
	
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