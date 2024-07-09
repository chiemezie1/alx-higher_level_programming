#!/usr/bin/python3
"""
A script that takes in a URL, sends a request to the URL, and displays
    the value of the X-Request-Id variable in the response header.
"""

import sys
import urllib.request

if __name__ == "__main__":
    with urllib.request.urlopen(sys.argv[1]) as response:
        print(response.info().get('X-Request-Id'))
