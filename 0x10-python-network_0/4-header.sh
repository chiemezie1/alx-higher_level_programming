#!/bin/bash
# A Bash script that takes in a URL as an argument, sends a GET request to the URL, and displays the body of the responses
curl -s "$1" -X GET -H "X-School-User-Id: 98"
