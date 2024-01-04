#!/usr/bin/python3
for i in range(122, 97, -1):
    if (i - 122) % 2 == 0:
        print("{}".format(chr(i)), end="")
    else:
        print("{}".format(chr(i - 32)), end="")
