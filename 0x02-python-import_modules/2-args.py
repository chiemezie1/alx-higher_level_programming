#!/usr/bin/python3
import sys
if __name__ == "__main__":
    args_count = len(sys.argv) - 1
    if args_count == 0:
        print("{:d} arguments.".format(args_count))
    else:
        if args_count == 1:
            print("{:d} argument:".format(args_count))
            print("{}: {}".format(args_count, sys.argv[args_count]))
        else:
            print("{:d} arguments:".format(args_count))
            for i in range(args_count):
                print("{}: {}".format(i + 1, sys.argv[i + 1]))
