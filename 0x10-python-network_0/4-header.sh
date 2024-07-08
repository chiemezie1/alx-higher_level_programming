#!/bin/bash
# A Bash script that demonstrates how to send a GET request with JSON data using curl

# Example URL (replace with your actual URL)
URL="$1"

# Example JSON data to send in the request body
JSON_DATA='{"X-School-User-Id": "98"}'

# Send the GET request with curl
curl -s \
     -X GET \
     -H "Content-Type: application/json" \
     -d "$JSON_DATA" \
     "$URL"
