#!/bin/bash
# A script that makes a request to 0.0.0.0:5000/catch_me to get a response containing "You got me!"
curl -sL -X GET "0.0.0.0:5000/catch_me" -o /dev/null -w "You got me!"
