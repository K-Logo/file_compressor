"""This file has all the classes for the tree programs.

This file is Copyright (c) 2023 Will Kukkamalla, Alex Lee, Kirill Logoveev, and Brandon Wong.
"""
from __future__ import annotations
from typing import Any, Optional


class Node:
    """
    Class for the Node data type.

    Instance Attributes:
    character: This stores the string for the character in the text file
    frequency: This is the number of Times that Character appears or the number of characters in the subtrees

    Represntation Invariants:
        - self.frequency > 0 and self.frequency is not None
        - isinstance(self.character, str)
    """
    character: Optional[str]
    frequency: int

    def __init__(self, c: Optional[str], f: int) -> None:
        """
        Initalizes the Node Object

        Precoditions:
            - isinstance(f, int)
            - f is not None and f > 0
        """
        if c is not None:
            self.character = c
        self.frequency = f

    def set_frequency(self, freq: int) -> None:
        """
        Sets the frequency of the node

        Preconditions:
            - isinstance(freq, int)
        """
        self.frequency = freq

    def set_character(self, char: str) -> None:
        """
        Changes the value for the character

        Preconditons:
            - isinstance(char, str)
            - self.character is not None
        """
        self.character = char

    def find_huffman_value(self, char: str, bits: str) -> str:
        """
        Finds the binary value for the given character

        Preconditions:
            - char is not None and isinstance(char, str)
        """
        if self.character == char:
            return bits
        else:
            return ""

    def find_character(self) -> str:
        """Returns the character in the stored in the node object."""
        return self.character


class HuffmanTree:
    """Contains the code for the huffman tree.

    Representation invariants:
        - self._root is Node or self._root is None or isinstance(self._root, int)

    """
    # Private Inttance Attributes:
    #    - _root:
    #       The root of the tree.
    #       It either represents the sum of characters from all of its subtrees or it contains a Node with the
    #       charactwhich means it's a leaf.
    #   - _left:
    #       The left subtree/node of the tree.
    #       If self._left is a Node object, then it is a leaf.
    #   - _right:
    #       The right subtree/node of the tree.
    #       If self._right is a Node object, then it is a leaf.

    _root: Optional[Node] | int
    _left: Optional[Node] | Optional[HuffmanTree]
    _right: Optional[Node] | Optional[HuffmanTree]

    def __init__(self, root: Optional[Node] | int) -> None:
        """Initializes a HuffmanTree by setting its _root and _left and _right subtrees.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = HuffmanTree(None)
            self._right = HuffmanTree(None)

    def add_subtrees(self, left: Optional[Node], right: Optional[Node]) -> None:
        """Adds subtrees to self.
        """
        if left is not None:
            self._left = left
        if right is not None:
            self._right = right

    def delete_subtrees(self) -> None:
        """Assigns the left and right subtrees to None.
        """
        self._left = None
        self._right = None

    def add(self, input_lst: list[Node]) -> None:
        """Creates the Huffman Tree by adding the nodes in list as leaves, and creates the intermediary nodes with the
        sum of frequencies from all of the subtrees below it.

        >>> tree = HuffmanTree(1)
        >>> tree.add([Node("c", 1), Node("a", 2),Node("b", 8),Node("d", 6),Node("g", 5),])
        >>> tree._root
        22

        >>> tree = HuffmanTree(1)
        >>> tree.add([Node("a", 1)])
        >>> tree.find_huffman_value("a", "")
        '0'
        """
        lst = []
        for node in input_lst:
            lst.append((node.frequency, node))

        if len(lst) == 1:
            self._root = lst[0][0]
            self._left = HuffmanTree(lst[0][1])
            self._left.delete_subtrees()
        else:
            while len(lst) != 1:
                min1_num = get_min(lst)
                min1 = lst.pop(lst.index(min1_num))
                min2_num = get_min(lst)
                min2 = lst.pop(lst.index(min2_num))

                tree = HuffmanTree(root=min1_num[0] + min2_num[0])

                tree.add_subtrees(min2[1], min1[1])

                lst.append((min1_num[0] + min2_num[0], tree))

            tree = lst[0][1]

            self._root = tree._root
            self._left = tree._left
            self._right = tree._right

    def get_root(self) -> Optional[Node] | Optional[int]:
        """Returns self._root.
        """
        return self._root

    def get_left(self) -> Optional[Node] | Optional[int]:
        """Returns self._left.
        """
        return self._left

    def get_right(self) -> Optional[Node] | Optional[int]:
        """Returns self._right.
        """
        return self._right

    def find_huffman_value(self, char: str, bits: str) -> str:
        """Returns the string of bits that represents char in the tree. Implemented recursively.

        Preconditions:
            - char is a valid ASCII character
            - bits == '' or all(bit == '0' or bit == '1' for bit in bits)

        >>> tree = HuffmanTree(1)
        >>> tree.add([Node("c", 1), Node("a", 2),Node("b", 8),Node("d", 6),Node("g", 5),])
        >>> lst = ["c", "a", "b", "d", "g"]
        >>> lst_2 = []
        >>> for i in lst:
        ...     x = tree.find_huffman_value(char=i, bits="")
        ...     lst_2.append(x)
        >>> lst_2
        ['0011', '0010', '1', '01', '000']
        """
        if self._left is None and self._right is None:
            if self._root is None:
                return ""
            if self._root.character == char:
                return bits
            else:
                return ""
        else:
            return self._left.find_huffman_value(char, bits + "0") + self._right.find_huffman_value(char, bits + "1")

    def tree_find_character(self, bits: str) -> Optional[str]:
        """Returns the character represented by the set of bits.

        >>> tree = HuffmanTree(1)
        >>> tree.add([Node("c", 1), Node("a", 2),Node("b", 8),Node("d", 6),Node("g", 5),])
        >>> tree.tree_find_character(bits="0011")
        'c'
        """
        if self._left is None and self._right is None:
            return self._root.character
        elif len(bits) == 0:
            return None
        elif bits[0] == '1':
            bits = bits[1:]
            if isinstance(self._right, Node):
                return self._right.find_character()
            else:
                return self._right.tree_find_character(bits)
        elif bits[0] == "0":
            bits = bits[1:]
            if isinstance(self._left, Node):
                return self._left.find_character()
            else:
                return self._left.tree_find_character(bits)
        else:
            return None

    def get_root_frequency(self) -> int:
        "Returns the integer stored in the root node of the tree"
        if isinstance(self._root, int):
            return self._root
        else:
            return self._root.frequency


def get_min(lst: list[tuple]) -> tuple:
    """Returns the tuple with the smallest first element.

    Preconditions:
        - all(isinstance(tup[0], int) for tup in list)
    """
    min_so_far = lst[0]
    for i in lst:
        if i[0] <= min_so_far[0]:
            min_so_far = i
    return min_so_far


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'typing'],
        'disable': ['unused-import', "too-many-function-args", "forbidden-import", "wildcard-import",
                    "inconsistent-return-statments", "unused_variables"]
    })
