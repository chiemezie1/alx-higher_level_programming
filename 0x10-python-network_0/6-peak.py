#!/usr/bin/python3
"""
A  function that finds a peak in a list of unsorted integers
"""
def find_peak(list_of_integers):
    """Find a peak element in a list of unsorted integers."""
    if not list_of_integers:
        return None

    def binary_search_peak(nums, left, right):
        if left == right:
            return nums[left]

        mid = (left + right) // 2

        if nums[mid] < nums[mid + 1]:
            return binary_search_peak(nums, mid + 1, right)
        else:
            return binary_search_peak(nums, left, mid)

    return binary_search_peak(list_of_integers, 0, len(list_of_integers) - 1)
