import numpy as np
from operator import add
from collections import defaultdict

# Burrows-wheeler transform is just a highly compressible bijective twister

base = "$abbababaababaaabaaa"
# base = 'appellee$'
query = "aaba"


def render_array(current_array):
    for elt in current_array:
        print elt
    print '----'


def bwt_forward(string):

    def roll_by_one(my_string):
        my_string = my_string[1:] + my_string[0]
        return my_string

    # TODO: use argsort to retrieve the indexes after a permutation

    accumulator = []

    for i in range(0, len(string)):
        accumulator.append(string)
        string = roll_by_one(string)

    sorting_arg = np.argsort(np.array(accumulator))
    location_index = np.arange(len(string))[sorting_arg]
    accumulator = sorted(accumulator)

    bwt_string = ''.join([elt[-1] for elt in accumulator])

    return location_index, bwt_string


def bwt_reverse(bwt_array):

    current_array = list(bwt_array)

    current_array = sorted(current_array)
    for i in range(0, len(bwt_array)-1):
        current_array = [a + b for a, b in zip(bwt_array, current_array)]
        current_array = sorted(current_array)

    return current_array[0]


def index(string):
    index_string = np.array(range(0, len(string)))
    char_dict = defaultdict(int)

    for i, char in enumerate(string):
        index_string[i] = char_dict[char]
        char_dict[char] += 1

    return index_string


def bwt_reverse_index(bwt_string):

    def read_orbit():
        collector = ['$']
        last_letter, last_letter_index = ['$', 0]
        for _ in range(0, len(bwt_string)-1):
            matching_mask = np.logical_and(last==last_letter, last_index==last_letter_index)
            last_letter, last_letter_index = (first[matching_mask][0], first_index[matching_mask][0])
            collector.append(str(last_letter))

        return collector

    last = bwt_string
    first = sorted(bwt_string)

    last_index = index(last)
    first_index = index(first)

    last = np.array(list(last))
    first = np.array(list(first))

    return ''.join(read_orbit())


def bwt_search(bwt_string, location_index, query):

    def match_query():

        rev_query = query[::-1]
        running_filter = first == rev_query[0]

        for to_char in rev_query[1:]:
            allowed_transitions = np.logical_and(running_filter, last == to_char)
            filtering_chars = last[allowed_transitions]
            filtering_idxs = last_index[allowed_transitions]

            running_filter.fill(False)
            for i, char in zip(filtering_chars.tolist(), filtering_idxs.tolist()):
                running_filter = np.logical_or(running_filter,
                                               np.logical_and(
                                                   first == i,
                                                   first_index == char
                                               ))

            if not np.any(running_filter):
                return []

        return location_index[running_filter].tolist()


    last = bwt_string
    first = sorted(bwt_string)

    last_index = index(last)
    first_index = index(first)

    last = np.array(list(last))
    first = np.array(list(first))

    return match_query()


def show_query(base, query, index_list):
    print base

    for index in sorted(index_list):
        print ''.join([' ']*index) + query


if __name__ == "__main__":
    location_index, bwt_array = bwt_forward(base)
    print bwt_array
    print bwt_reverse_index(bwt_array)
    search_list = bwt_search(bwt_array, location_index, query)
    show_query(base, query, search_list)