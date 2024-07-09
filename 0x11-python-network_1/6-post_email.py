#!/usr/bin/python3
"""
Take a URL and an Email and sends a POST request
"""
import requests
import sys

if __name__ == "__main__":
    url = sys.argv[1]
    email = sys.argv[2]
    data = {"email": email}
    r = requests.post(url, data)
    print(r.text)
