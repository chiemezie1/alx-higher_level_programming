#!/usr/bin/python3
from sys import argv
from calculator_1 import add, sub, mul, div
if __name__ == "__main__":
    ags = len(argv)
    if ags != 4:
        print("Usage: ./100-my_calculator.py <a> <operator> <b>")
        exit(1)
    else:
        opr = argv[2]
        if opr not in ["+", "-", "*", "/"]:
            print("Unknown operator. Available operators: +, -, * and /")
            exit(1)

            agsA = int(argv[1])
            agsB = int(argv[3])
        
            if opr == "+":
                print("{:d} + {:d} = {:d}".format(agsA, agsB, add(agsA, agsB)))
            elif opr == "-":
                print("{:d} - {:d} = {:d}".format(agsA, agsB, sub(agsA, agsB)))
            elif opr == "*":
                print("{:d} * {:d} = {:d}".format(agsA, agsB, mul(agsA, agsB)))
            elif opr == "/":
                print("{:d} / {:d} = {:d}".format(agsA, agsB, div(agsA, agsB)))
            exit(0)
