#!/usr/bin/python3
""""
Takes a URL and an Email and sends a POST request and email as a parameter to the URL
"""
import sys
import urllib.request

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <email>".format(sys.argv[0]))
        sys.exit(1)

    email = sys.argv[2]
    data = urllib.parse.urlencode({"email": email}).encode("ascii")
    req = urllib.request.Request(sys.argv[1], data)
    with urllib.request.urlopen(req) as response:
        print(response.read().decode("utf-8"))
