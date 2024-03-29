#!/usr/bin/python3
"""importing sys"""
import sys

"""
script that adds all arguments to a Python list
and save them to a file

"""


if __name__ == "__main__":
    to_json = __import__('5-save_to_json_file')
    from_json = __import__('6-load_from_json_file')

    save_to_json_file = to_json.save_to_json_file
    load_from_json_file = from_json.load_from_json_file

    try:
        my_list = load_from_json_file("add_item.json")
    except FileNotFoundError:
        my_list = []
    for i in range(1, len(sys.argv)):
        my_list.append(sys.argv[i])
    save_to_json_file(my_list, "add_item.json")
