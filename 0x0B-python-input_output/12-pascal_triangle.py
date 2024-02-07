#!/usr/bin/python3
"""
returns a list of lists of integers 
representing the Pascal’s triangle of n

"""


def pascal_triangle(n):
    """
    returns a list of lists of integers 
    representing the Pascal’s triangle
    """
    list_of_triangle = []
    if n <= 0:
        return list_of_triangle
    else:
        list_of_triangle.append([1])
        for i in range(1, n):
            new_list = [1]
            for j in range(0, i - 1):
                new_list.append(list_of_triangle[i - 1][j] +
                                list_of_triangle[i - 1][j + 1])
            new_list.append(1)
            list_of_triangle.append(new_list)
        return list_of_triangle
