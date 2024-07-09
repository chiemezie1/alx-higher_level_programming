#!/usr/bin/`python3
"""
Script that takes your Github credentials (username and password)
and uses the Github API to display your id
"""
import requests
import sys

if __name__ == "__main__":
    username = sys.argv[1]
    token = sys.argv[2]
    url = 'https://api.github.com/user'

    response = requests.get(url, auth=(username, token))
    if response.status_code == 200:
        user_info = response.json()
        print(user_info.get('id'))
    else:
        print(None)
