#!/bin/bash
# Sends a GET request to the URL and displays the body of a 200 status code response

URL=$1
curl -s -o response_body -D response_headers "$URL"

# Check if the response headers contain a 200 status code
if grep -q "200 OK" response_headers; then
    cat response_body
fi

# Clean up temporary files
rm response_body response_headers
