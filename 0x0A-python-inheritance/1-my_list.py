#!/usr/bin/python3

""""my_list module

inherits from list

"""


class MyList(list):
    """my_list class

    inherits from list

    Public instance method: print_sorted

    """

    def print_sorted(self):
        """prints the list, but sorted (ascending sort)"""
        print(sorted(self))
