import numpy as np
from operator import add

# base = "abbababaababaaabaaa"
base = 'appellee$'
query = "aaba"


def render_array(current_array):
    for elt in current_array:
        print elt
    print '----'


def bwt_forward(string):

    def roll_by_one(my_string):
        my_string = my_string[1:] + my_string[0]
        return my_string

    accumulator = []

    for i in range(0, len(string)):
        accumulator.append(string)
        string = roll_by_one(string)

    accumulator = sorted(accumulator)

    return ''.join([elt[-1] for elt in accumulator])


def bwt_reverse(bwt_array):

    current_array = list(bwt_array)

    current_array = sorted(current_array)
    for i in range(0, len(bwt_array)-1):
        current_array = [a + b for a, b in zip(bwt_array, current_array)]
        current_array = sorted(current_array)

    return current_array[0]


def bwt_search(bwt_array):
    pass


if __name__ == "__main__":
    bwt_array = bwt_forward(base)
    print bwt_array
    print bwt_reverse(bwt_array)