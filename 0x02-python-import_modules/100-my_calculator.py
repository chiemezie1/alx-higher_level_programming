#!/usr/bin/python3
from sys import argv
from calculator_1 import add, sub, mul, div

if __name__ == "__main__":
    ags = len(argv)
    if ags != 4:
        print("Usage: ./100-my_calculator.py <a> <operator> <b>")
        exit(1)
    else:
        agsA = int(argv[1])
        opr = argv[2]
        agsB = int(argv[3])

        if opr not in ["+", "-", "*", "/"]:
            print("Unknown operator. Available operators: +, -, * and /")
            exit(1)

        if opr == "+":
            print("{:d} + {:d} = {:d}".format(agsA, agsB, add(agsA, agsB)))
        elif opr == "-":
            print("{:d} - {:d} = {:d}".format(agsA, agsB, sub(agsA, agsB)))
        elif opr == "*":
            print("{:d} * {:d} = {:d}".format(agsA, agsB, mul(agsA, agsB)))
        elif opr == "/":
            if agsB == 0:
                print("Error: Division by zero")
                exit(1)
            print("{:d} / {:d} = {:d}".format(agsA, agsB, div(agsA, agsB)))
        else:
            print("Unknown error occurred")
            exit(1)
        exit(0)
