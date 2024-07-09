#!/usr/bin/python3
"""
Takes a letter and sends a POST request to http://0.0.0.0:5000/search_user
    with the letter as a parameter.
    The letter must be sent in the variable q
"""
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        letter = sys.argv[1]
    else:
        letter = ""
    payload = {"q": letter}
    r = requests.post("http://0.0.0.0:5000/search_user", data=payload)
    try:
        r_json = r.json()
        if r_json:
            print("[{}] {}".format(r_json["id"], r_json["name"]))
        else:
            print("No result")
    except ValueError:
        print("Not a valid JSON")
