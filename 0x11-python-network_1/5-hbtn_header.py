#!/usr/bin/python3
"""
Takes a URL and sends a request to the URL and displays X-Request-Id
"""
import sys
import requests

if __name__ == "__main__":
    url = sys.argv[1]
    r = requests.get(url)
    print(r.headers.get('X-Request-Id'))
