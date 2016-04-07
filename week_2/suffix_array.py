import numpy as np

base = "abbababaababaaabaaa"
query = "aaba"

array = []
array_n = []

def binary_array_search(query):

    def expand_central(index):
        accumulator = [index]

        running_index = index+1

        while len(array[running_index]) >= query_len and array[running_index][:query_len] == query:
            accumulator.append(running_index)
            running_index += 1

        running_index = index - 1

        while len(array[running_index]) >= query_len and array[running_index][:query_len] == query:
            accumulator.append(running_index)
            running_index -= 1

        return accumulator


    running_bounds = [0, len(array)]
    query_len = len(query)

    while True:
        anchor = (running_bounds[1]-running_bounds[0])/2+running_bounds[0]
        # print anchor, array[anchor], query

        if len(array[anchor]) >= query_len and array[anchor][:query_len] == query:
            # print "matched %s @ %s" % (array[anchor], anchor)
            return expand_central(anchor)

        else:
            if array[anchor] > query:
                # print 'resetting upper running bounds', anchor
                running_bounds[1] = anchor
            else:
                # print 'resetting lower running bounds', anchor
                running_bounds[0] = anchor

        if running_bounds[1] - running_bounds[0] == 0:
            return []


def show_query(base, query, index_list):
    print base

    for index in sorted(index_list):
        print ''.join([' ']*index) + query


max_n = 0
for sub_str_len in range(1, len(base)-1):
    array.append(base[-sub_str_len:])
    array_n.append(len(base)-sub_str_len)

array = np.array(array)
array_n = np.array(array_n)

argsort = np.argsort(array)
array = array[argsort]
array_n = array_n[argsort]

# print array
# print array_n

res_list = binary_array_search(query)

res_list = array_n[res_list]

show_query(base, query, res_list)