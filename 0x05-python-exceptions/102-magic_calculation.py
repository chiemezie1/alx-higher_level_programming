#!/usr/bin/python3

def magic_calculation(a, b):
    result = 0

    for i in range(1, 3):
        try:
            if i > len(a):
                raise Exception('Too far')

            result += (a[i] ** b[i]) / i

        except Exception:
            result += a[i] + b[i]
            break

    return result
