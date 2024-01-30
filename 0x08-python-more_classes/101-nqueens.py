#!/usr/bin/python3
import sys

def is_safe(board, row, col, N):
    """Check if it's safe to place a queen at board[row][col]"""
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

def solve_nqueens(board, row, N, solutions):
    """Recursively solve N Queens problem and print solutions"""
    if row == N:
        solutions.append([[i, board[i]] for i in range(N)])
    else:
        for col in range(N):
            if is_safe(board, row, col, N):
                board[row] = col
                solve_nqueens(board, row + 1, N, solutions)

def print_solutions(N):
    """Print all solutions for N Queens problem"""
    board = [-1] * N
    solutions = []
    solve_nqueens(board, 0, N, solutions)
    
    for solution in solutions:
        print(solution)
