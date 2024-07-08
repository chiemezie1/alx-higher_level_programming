#!/bin/bash
# Sends a GET request to the URL and displays the body of a 200 status code response

URL=$1

# Send GET request and capture the HTTP status code
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")

# If the HTTP status code is 200, then display the response body
if [ "$HTTP_STATUS" -eq 200 ]; then
    curl -s "$URL"
fi
