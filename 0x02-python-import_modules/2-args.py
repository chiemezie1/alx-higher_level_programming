#!/usr/bin/python3
import sys
print("{} arguments:".format(len(sys.arg)))
for i in range(1, len(sys.argv)):
    print("{}: {}".format(i, sys.argv[i]))
