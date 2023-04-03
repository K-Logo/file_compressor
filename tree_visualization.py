"""This is the module for visualizing a Huffman Tree.

This file is Copyright (c) 2023 Will Kukkamalla, Alex Lee, Kirill Logoveev, and Brandon Wong.
"""
import pydot
from IPython.display import Image, display
from tree import HuffmanTree, Node
import pandas as pd


def key_to_tree(key: str) -> HuffmanTree:
    """Takes in a csv file of a Huffman Tree, returns a HuffmanTree object

    Preconditions:
        - key is the name of a valid Huffman Tree csv file
    """
    key_lst = []
    key_csv = pd.read_csv(key)
    for i, row in key_csv.iterrows():
        key_lst.append(Node(row["Character"], row["Frequency"]))
    # Creates the tree to decode the text
    tree = HuffmanTree(1)
    tree.add(key_lst)
    return tree


def tree_to_svg(G: pydot.Dot, tree: HuffmanTree, visited_names: set, identifier: int) -> None:
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
    if isinstance(tree.get_root(), int):
        node = pydot.Node(name=root_name, label=str(tree.get_root()))
        G.add_node(node)
    elif isinstance(tree.get_root(), Node):
        node = pydot.Node(name=root_name, label=str(tree.get_root().frequency))
        G.add_node(node)

    if tree.get_left() is not None:
        if isinstance(tree.get_left(), HuffmanTree):
            # Recurse into the left subtree
            tree_to_svg(G, tree.get_left(), visited_names, new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='0')
            G.add_edge(edge)
        elif isinstance(tree.get_left(), Node):
            # Note that we cannot recurse into a Node object
            node = pydot.Node(name=str(new_identifier),
                              label=str(tree.get_left().frequency) + ' ' + tree.get_left().character)
            G.add_node(node)
            visited_names.add(new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='0')
            G.add_edge(edge)

    # Refresh new_identifier
    while new_identifier in visited_names:
        new_identifier += 1

    if tree.get_right() is not None:
        if isinstance(tree.get_right(), HuffmanTree):
            # Recurse into the right subtree
            tree_to_svg(G, tree.get_right(), visited_names, new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='1')
            G.add_edge(edge)
        elif isinstance(tree.get_right(), Node):
            # Note that we cannot recurse into a Node object
            node = pydot.Node(name=str(new_identifier),
                              label=str(tree.get_right().frequency) + ' ' + tree.get_right().character)
            G.add_node(node)
            visited_names.add(new_identifier)
            edge = pydot.Edge(root_name, str(new_identifier), label='1')
            G.add_edge(edge)

G = pydot.Dot(graph_type="digraph")
G.size = "7.75,10.25"

tree_file_name = input("Type in the file name of the Huffman Tree csv file. "
                       "Make sure it is in the same directory as tree_visualization. (Type the file name without"
                       "the .csv extension)")
# Example tree
tree = key_to_tree(tree_file_name+'.csv')

tree_to_svg(G, tree, set(), 0)

im = Image(G.create_svg())

display(im)

G.write_svg('graph.svg')


