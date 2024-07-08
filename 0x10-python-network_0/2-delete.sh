#!/bin/bash
# A script that sends a DELETE request to the URL passed as an argument, and displays the body of the response
curl -sX DELETE "$1" 
