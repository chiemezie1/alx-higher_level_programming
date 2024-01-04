#!/usr/bin/python3
import sys
if __name__ == "__main__":
    args_count = len(sys.argv) - 1
    sum_args = 0
    for i in range(args_count):
        sum_args += int(sys.argv[i + 1])
    print(sum_args)
