import pydot

base = "abbababaababaaabaaa"
query = "aaba"

suffix_tree = {0:[[],[], None]}
# Node # -> [[suffix, suffix,],[Node#, Node#,], termination]
# root is guaranteed to have index 0

# three stages:
#   - generate the tree from the start
#   - for each repeating subpattern


def render_tree(tree):
    graph = pydot.Dot(graph_type='graph')
    for key, pointer in tree.iteritems():
        print key, pointer
        edge = pydot.Edge("%s" % key, "%s" % pointer)
        graph.add_edge(edge)
    graph.write_png('tree_rendering.png')


def add_to_tree(tree, suffix, index, max_nn):
    running_tree_index = 0
    suffix_index = 0

    for breaking_index, char in enumerate(suffix):
        if char in tree[running_tree_index][0]:
            running_tree_index = tree[running_tree_index][1][
                tree[running_tree_index][0].index(char)]
            suffix_index = breaking_index
        else:
            break

    if suffix_index == len(suffix) - 1:  # TODO: breaks here
        if index != tree[running_tree_index][3] != index:
            raise Exception('Suffix already exist!')
        else:
            return max_nn

    for node_nn, char in zip(range(max_nn + 1), suffix[suffix_index+1:]):
        tree[running_tree_index][0].append(char)
        tree[running_tree_index][1].append(node_nn)
        tree[node_nn] = [[], [], None]
        running_tree_index = node_nn

    tree[running_tree_index][2] = index

    # tree is mutable, so we don't need to return it
    return running_tree_index


def collapse_lines(tree):
    pass


for sub_str_len in range(1, len(base)-1):
    max_n = add_to_tree(suffix_tree, base[-sub_str_len:], len(base)-sub_str_len, 0)

suffix_tree["%s - %s" % (base[-1], len(base)-1)] = '$ - 0'

render_tree(suffix_tree)

