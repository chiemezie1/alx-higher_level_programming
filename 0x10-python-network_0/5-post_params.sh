#!/bin/bash
# A script that takes in a URL, sends a POST request to the passed URL, and displays the body of the response
curl -s "$1" -X POST -d "test@gmail.com&subject=I will always be here for PLD"
