import pydot
from itertools import count

base = "abbababaababaaabaaa"
query = "aaba"

suffix_tree = {0: [[], [], None]}
# Node # -> [[suffix, suffix,],[Node#, Node#,], termination]
# root is guaranteed to have index 0

# three stages:
#   - generate the tree from the start
#   - for each repeating subpattern


def render_tree(tree):
    graph = pydot.Dot(graph_type='graph')
    for key, (pointer_names, pointers, match_termination) in tree.iteritems():
        for ponter_name, pointer in zip(pointer_names, pointers):
            edge = pydot.Edge(key, pointer, label=ponter_name)
            graph.add_edge(edge)
        if match_termination is not None:
            edge = pydot.Edge(key, "$ @ %s" % match_termination)
            graph.add_edge(edge)
    graph.write_png('tree_rendering.png')


def add_to_tree(tree, suffix, index, max_nn):
    running_tree_index = 0
    suffix_index = -1

    # print 'inserting suffix', suffix

    for breaking_index, char in enumerate(suffix):
        if char in tree[running_tree_index][0]:
            # print '\t char %s -> index in suffix %s' % (char, breaking_index)
            running_tree_index = tree[running_tree_index][1][
                tree[running_tree_index][0].index(char)]
            suffix_index = breaking_index
            # print ' \t running tree index: %s, suffix_index: %s' % (running_tree_index,
            #                                                         suffix_index)
        else:
            break

    # print 'suffix index', suffix_index
    # print 'suffix len', len(suffix)
    # print 'tree matched index: %s -> %s' % (running_tree_index, tree[running_tree_index])

    if suffix_index == len(suffix) - 1:  # TODO: breaks here
        # print 1
        if tree[running_tree_index][2] and index != tree[running_tree_index][2] != index:
            # print 1.1
            raise Exception('Suffix already exist!')
        else:
            # print 1.2
            return max_nn

    # print max_nn, suffix_index, running_tree_index
    # print zip(count(max_nn + 1), suffix[suffix_index + 1:])

    for node_nn, char in zip(count(max_nn + 1), suffix[suffix_index + 1:]):
        # print '\t inserting %s into node %s' % (char, node_nn)
        # print '\t pre-insertion: %s -> %s' % (running_tree_index, tree[running_tree_index])
        tree[node_nn] = [[], [], None]
        tree[running_tree_index][0].append(char)
        tree[running_tree_index][1].append(node_nn)
        # print '\t post-insertion: %s -> %s' % (running_tree_index, tree[running_tree_index])
        running_tree_index = node_nn

    tree[running_tree_index][2] = index

    # tree is mutable, so we don't need to return it
    # print '=>\n\t%s\n%s' % (tree, running_tree_index)

    # raw_input('press enter to continue')

    return running_tree_index


def collapse_linear_segments(tree):

    def walk_linear_segments(node):
        _, link_list, termination = tree[node]

        if len(link_list) == 1 and not termination:  # we are in a linear segment
                return [node] + walk_linear_segments(link_list[0])

        return [node]

    def compact_linear_segment(node_list, parent_node):
        # print "compacting %s with parent %s" % (node_list, parent_node)
        finishing_index = node_list[-1]
        # print 'pre_compaction: %s -> %s' % (parent_node, tree[parent_node])
        letter_index = tree[parent_node][1].index(node_list[0])
        collection_string = [tree[parent_node][0][letter_index]]
        for node in reversed(node_list[:-1]):
            # problem: the linear list should contain the bifurcating node! => call memory
            collection_string.append(tree[node][0][0])
            del tree[node]
        collection_string = ''.join(collection_string)
        tree[parent_node][0][letter_index] = collection_string
        tree[parent_node][1][letter_index] = finishing_index
        # print 'post_compaction: %s -> %s' % (parent_node, tree[parent_node])
        # raw_input('linear compaction finished: press enter to continue')

    def compact_subtree(compaction_tree_root, parent_node):
        node_list = walk_linear_segments(compaction_tree_root)
        # print "linear walk on %s : %s" % (compaction_tree_root, node_list)

        if parent_node == None and len(node_list) > 1:
            # print 'parent reset in %s' % node_list
            parent_node = node_list[0]
            node_list = node_list[1:]

        if len(node_list) > 1:
            compact_linear_segment(node_list, parent_node)

        final_node = node_list[-1]

        # print 'final_node:', final_node

        _, link_list, _ = tree[final_node]
        for subnode in link_list:
            # print "calling compaction on %s with parent %s" % (subnode, final_node)
            compact_subtree(subnode, final_node)

            # todo: reset compaction on a node

        # raw_input('subtree compaction on root %s finished: press enter to continue' % compaction_tree_root)

    compact_subtree(0, None)


def collect_leaves(tree, node):
    _, link_list, termination = tree[node]

    if termination:
        return [termination]

    else:
        collection_list = []
        for subnode in link_list:
            collection_list += collect_leaves(tree, subnode)
        return collection_list


def match_query(tree, query):
    """
    Can operate only on non-compacted trees

    :param tree:
    :param query:
    :return:
    """
    running_tree_index = 0

    # print 'searching for query:', query

    for breaking_index, char in enumerate(query):
        if char in tree[running_tree_index][0]:
            # print '\t char %s -> index in suffix %s' % (char, breaking_index)
            running_tree_index = tree[running_tree_index][1][
                tree[running_tree_index][0].index(char)]
            suffix_index = breaking_index
            # print ' \t running tree index: %s, suffix_index: %s' % (running_tree_index,
            #                                                         suffix_index)

    if suffix_index and suffix_index == len(query)-1:
        return collect_leaves(tree, running_tree_index)

    else:
        return []


def show_query(base, query, index_list):
    print base

    for index in sorted(index_list):
        print ''.join([' ']*index) + query


max_n = 0
for sub_str_len in range(1, len(base)-1):
    max_n = add_to_tree(suffix_tree, base[-sub_str_len:], len(base)-sub_str_len, max_n)

match_list = match_query(suffix_tree, query)

show_query(base, query, match_list)

# collapse_linear_segments(suffix_tree)

# render_tree(suffix_tree)

