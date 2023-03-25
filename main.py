"""
This file is the main file for the text compressor
"""
from tree import Node, HuffmanTree
def open_file(file:str)-> dict():
    """
    >>> open_file("test.txt")
    :param file:
    :return:
    """
    frequency = {}
    with open(file) as f:
        lines = f.readlines()
        for i in lines:
            for j in i:
                if j not in frequency:
                    frequency[j] = 0
                else:
                    frequency[j] += 1
    return frequency

if __name__ == '__main__':
    dict = open_file("test.txt")
    lst = []
    for i in dict:
        lst.append(Node(i, dict[i]))
    # tree = HuffmanTree()
    # tree.add(lst)



