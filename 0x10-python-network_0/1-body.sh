#!/bin/bash
# This program takes in a URL, sends a GET request to the URL, and displays the body of the response.
curl -sL "$1" -X GET -D ./response_header -o ./response_output; if grep -q "200 OK" ./header; then cat ./output; fi

rm ./response_header ./response_output