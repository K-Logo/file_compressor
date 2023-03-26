"""
This file is the main file for the text compressor
"""
from tree import Node, HuffmanTree
from math import ceil
import codecs
import struct

def open_file(file:str)-> dict():
    """
    >>> open_file("test.txt")
    :param file:
    :return:
    """
    frequency = {}
    with codecs.open(file, encoding="utf-8") as f:
        lines = f.readlines()
        for i in lines:
            for j in i:
                if j not in frequency:
                    frequency[j] = 0
                else:
                    frequency[j] += 1
    return frequency

def get_binary_values(tree, letters)-> dict():
    values = {}
    for i in letters:
        value = tree.find_huffman_value(i, "")
        values[i] = value
    return values

def encode(file:str):
    # Reads the file and returns a dictionary with all of the letters and their frequencies
    dict = open_file("test.txt")
    letters = []
    # Creates the tree
    lst = []
    for i in dict:
        lst.append(Node(i, dict[i]))
        letters.append(i)
    tree = HuffmanTree(1)
    tree.add(lst)

    values = get_binary_values(tree, letters)

    bits_so_far = 0

    string = ""

    # Read through the input file
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            for character in line:
                # for every character, get their bitset, and set those numbers to the bits_out
                # Nuance: the bits_out are cast to be a Byte Array, and then it's written to the output file

                sequence_bits = values[character]

                string += sequence_bits

            with open("output.bnr", "wb") as o:
                o.write(int(string[::-1], 2).to_bytes(ceil(len(string) / 8), 'little'))
                #o.write(bytes(string[::-1].encode()))
    return lst

def decode(file: str, key: list):
    #Creates the tree to decode the text
    tree = HuffmanTree(1)
    tree.add(key)

    # Opens the file to decode the text
    with open(file, "rb") as f:


        lines = f.readlines()

        # Iterates the throuh the file to get the bytes
        line_so_far = ""
        string_so_far = ""
        with open("outputtext.txt", "w") as o:
            for line in lines:

                # Turns the byte into a string of either 0 or 1
                x = format(int.from_bytes(line, 'little'), '023b')[::-1]
                line = str(x)

                # iterates though every single one or zero
                for charater in line:
                    string_so_far = string_so_far + charater
                    char = tree.find_character(string_so_far)

                    # if the char is found then it resets the string to find the next character
                    if char is not None:

                        line_so_far = line_so_far + string_so_far
                        string_so_far = ""
                        o.write(char)


if __name__ == '__main__':
    # Reads the file and returns a dictionary with all of the letters and their frequencies
    key = encode("test.txt")
    decode("output.bnr", key)
