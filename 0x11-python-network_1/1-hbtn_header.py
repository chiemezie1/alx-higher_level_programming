#!/usr/bin/python3
""""
A script that takes in URL, send a request to the URL and displays
    the value of the X-Request-Id variable in the response header
"""
import sys
import urllib.request

with urllib.request.urlopen(sys.argv[1]) as response:
    print(response.getheader('X-Request-Id'))
