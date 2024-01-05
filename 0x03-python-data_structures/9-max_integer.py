#!/usr/bin/python3
def max_integer(my_list=[]):
    maxInt = 0
    length_list = len(my_list)
    for i in range(length_list):
        if my_list[i] > maxInt:
            maxInt = my_list[i]
    return maxInt
