#!/usr/bin/python3
def multiply_by_2(a_dictionary):
    b_dictionary = a_dictionary.copy()
    for k, v in b_dictionary.items():
        b_dictionary[k] = 2 * v
    return b_dictionary
