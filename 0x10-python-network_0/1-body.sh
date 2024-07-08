#!/bin/bash
# Sends a GET request to the URL and displays the body of a 200 status code response

curl -sL "$1" -X GET -D ./header -o ./body; if grep -q "200 OK" ./header; then cat ./output; fi
