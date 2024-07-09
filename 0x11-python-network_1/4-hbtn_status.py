#!/usr/bin/python3
"""
A script that fetches ALX intranet status using requests
"""
import sys
import requests

if __name__ == "__main__":
    url = "https://alx-intranet.hbtn.io/status"
    r = requests.get(url)
    print("Body response:")
    print("\t- type: {}".format(r.headers['content-type']))
    print("\t- content: {}".format(r.encoding))
    