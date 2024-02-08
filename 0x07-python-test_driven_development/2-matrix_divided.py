#!/usr/bin/python3
"""
fuction that divie all element of a matrix
"""


def matrix_divided(matrix, div):
    """
    Write a function that divides all elements of a matrix
    """

    error_msg = "matrix must be a matrix (list of lists) of integers/floats"
    error_msg_row = "Each row of the matrix must have the same size"
    error_msg_non_empty = "matrix must be a non-empty matrix (list of lists)"
    error_msg_div = "div must be a number"
    error_msg_zero = "division by zero"

    if not matrix or not all(matrix):
        raise TypeError(error_msg_non_empty)

    row_length = len(matrix[0])

    for row in matrix:
        if len(row) != row_length:
            raise TypeError(error_msg_row)

        for element in row:
            if not isinstance(element, (int, float)):
                raise TypeError(error_msg_list)

    if not isinstance(div, (int, float)):
        raise TypeError(error_msg_div)

    if div == 0:
        raise ZeroDivisionError(error_msg_zero)
    result = element / div
    result_matrix = [[round(result, 2) for element in row] for row in matrix]
    return result_matrix
