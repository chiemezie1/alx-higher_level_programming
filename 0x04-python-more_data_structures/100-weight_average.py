#!/usr/bin/python3
def weight_average(my_list=[]):
    for i in my_list:
        if i[0] == 0:
            return 0
    sum = 0
    for i in my_list:
        sum += i[0] * i[1]
    return sum / sum(i[0] for i in my_list)
