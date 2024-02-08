#!/usr/bin/python3
"""
fuction that divie all element of a matrix
"""


def matrix_divided(matrix, div):
    """
    Write a function that divides all elements of a matrix
    """
    if not matrix or not all(matrix):
        raise TypeError('matrix must be a non-empty matrix (list of lists)')

    row_length = len(matrix[0])

    for row in matrix:
        if len(row) != row_length:
            raise TypeError('Each row of the matrix must have the same size')

        for element in row:
            if not isinstance(element, (int, float)):
                raise TypeError('matrix must be a matrix (list of lists) of integers/floats')

    if not isinstance(div, (int, float)):
        raise TypeError('div must be a number')

    if div == 0:
        raise ZeroDivisionError('division by zero')

    result_matrix = [[round(element / div, 2) for element in row] for row in matrix]
    
    return result_matrix
