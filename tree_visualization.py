import pydot
from IPython.display import Image, display
from tree import HuffmanTree, Node


G = pydot.Dot(graph_type="digraph")
G.size = "7.75,10.25"

# Example tree
tree = HuffmanTree(1)
tree.add([Node("c", 1), Node("a", 2), Node("b", 8), Node("d", 6), Node("g", 5), Node('z', 500), Node('k', 32), Node('q', 100), Node('.', 200), Node('j', 32)])

identifier = 0
visited_names = set()


def add_nodes_and_edges(G: pydot.Dot, tree: HuffmanTree, visited_names: set, identifier: int) -> None:
    """Takes in a directed graph and a huffman tree, adds the nodes and edges
    of the Huffman tree to the graphviz directed graph object.

    visited_names keeps track of the names (identifiers) of the nodes already used, to make sure the nodes'
    names are not duplicated. Note that the names for the node objects are merely unique identifiers; they are not
    actually displayed on the graph.

    Preconditions:
        - identifier not in visited_names
        - all(isinstance(element, str) for element in visited_names)
        - all elements in visited_names are strings of natural numbers
    """
    visited_names.add(identifier)

    # new_identifier will be the name of the child nodes
    new_identifier = identifier + 1
    while new_identifier in visited_names:
        new_identifier += 1
    visited_names.add(new_identifier)
    root_name = str(identifier)

    # Add the root to dot
    if isinstance(tree._root, int):
        node = pydot.Node(name=root_name, label=str(tree._root))
        G.add_node(node)
    elif isinstance(tree._root, Node):
        node = pydot.Node(name=root_name, label=str(tree._root.frequency))
        G.add_node(node)

    if tree._left is not None:
        if isinstance(tree._left, HuffmanTree):
            # Recurse into the left subtree
            add_nodes_and_edges(G, tree._left, visited_names, new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='0')
            G.add_edge(edge)
        elif isinstance(tree._left, Node):
            # Note that we cannot recurse into a Node object
            node = pydot.Node(name=str(new_identifier), label=str(tree._left.frequency)+ ' ' + tree._left.character)
            G.add_node(node)
            visited_names.add(new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='0')
            G.add_edge(edge)

    # Refresh new_identifier
    while new_identifier in visited_names:
        new_identifier += 1

    if tree._right is not None:
        if isinstance(tree._right, HuffmanTree):
            # Recurse into the right subtree
            add_nodes_and_edges(G, tree._right, visited_names, new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='1')
            G.add_edge(edge)
        elif isinstance(tree._right, Node):
            # Note that we cannot recurse into a Node object
            node = pydot.Node(name=str(new_identifier), label=str(tree._right.frequency)+ ' ' + tree._right.character)
            G.add_node(node)
            visited_names.add(new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='1')
            G.add_edge(edge)




add_nodes_and_edges(G, tree, set(), 0)

im = Image(G.create_svg())

display(im)

G.write_svg("treegraph.svg")
