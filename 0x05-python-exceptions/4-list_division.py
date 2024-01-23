#!/usr/bin/python3
def list_division(my_list_1, my_list_2, list_length):
    new_list = []
    try:
        for i in range(list_length):
            if type(my_list_1[i]) is int or type(my_list_1[i]) is float:
                if type(my_list_2[i]) is int or type(my_list_2[i]) is float:
                    new_list.append(my_list_1[i] / my_list_2[i])
                else:
                    new_list.append(0)
                    raise TypeError
            else:
                new_list.append(0)
                raise TypeError
    except ZeroDivisionError:
        print("division by 0")
    except TypeError:
        print("wrong type")
    except IndexError:
        print("out of range")
    finally:
        return new_list
    