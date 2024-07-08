#!/bin/bash
# A script that makes a request to 0.0.0.0:5000/catch_me to get a response containing "You got me!"
curl -sL -X PUT -d "user_id=98" -H "Origin: You got me!" "0.0.0.0:5000/catch_me"
