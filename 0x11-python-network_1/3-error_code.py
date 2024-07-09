#!/ur/bin/python3
"""
Takes a URL and sends a request to the URL and displays the
    body of the response
"""
import urllib.request
import sys

if __name__ == "__main__":
    if len(sys.argv) > 2:
        url = sys.argv[1]
        try:
            with urllib.request.urlopen(url) as response:
                print(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print("Error code: {}".format(e.code))
