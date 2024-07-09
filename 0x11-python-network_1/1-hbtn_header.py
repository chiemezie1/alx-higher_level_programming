#!/usr/bin/python3
""""
A script that takes in URL, send a request to the URL and displays the value
"""
import sys
import urllib.request

if sys.argv[1]:
    with urllib.request.urlopen(sys.argv[1]) as response:
        print(response.info()['X-Request-Id'])
