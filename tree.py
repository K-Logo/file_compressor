from typing import Any, Optional
# from Bitset import Bitset


class Node:
    "Class for the Node data type."
    character: Optional[str]
    frequency: int

    def __init__(self, c, f) -> None:
        if c is not None:
            self.character = c
        self.frequency = f

    def set_frequency(self, freq: int) -> None:
        """Sets the frequency of the node"""
        self.frequency = freq

    def set_character(self, char: str) -> None:
        self.character = char

    def find_huffman_value(self, char: str, bits: str) -> str:
        if self.character == char:
            return bits
        else:
            return ""


class HuffmanTree:
    "Contains the code for the huffman tree"
    _root: Optional[Node]

    def __init__(self, root: Optional[int]) -> None:
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = HuffmanTree(None)
            self._right = HuffmanTree(None)

    def add_subtrees(self, left: Optional[Node], right:Optional[Node]):
        if left is not None:
            self._left = left
        if right is not None:
            self._right = right


    def add(self, og_lst: list[Node]):
        """
        >>> tree = HuffmanTree(1)
        >>> tree.add([Node("c", 1), Node("a", 2),Node("b", 8),Node("d", 6),Node("g", 5),])
        >>> tree._root
        22
        >>> type(tree._left)
        >>> tree._right

        """
        lst = []
        for node in og_lst:
            lst.append((node.frequency, node))

        while len(lst) != 1:
            min1_num = get_min(lst)
            min1 = lst.pop(lst.index(min1_num))
            min2_num = get_min(lst)
            min2 = lst.pop(lst.index(min2_num))

            tree = HuffmanTree(root= min1_num[0] + min2_num[0])

            tree.add_subtrees(min2[1], min1[1])

            lst.append((min1_num[0] + min2_num[0], tree))

        tree = lst[0][1]

        self._root = tree._root
        self._left = tree._left
        self._right = tree._right


    def insert(self, node):
        if self._left is None:
             self._left = HuffmanTree(node)
        elif self._right is None:
            self._right= HuffmanTree(node)

    def find_huffman_value(self, char: str, bits: str) -> str:
        """
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
            if self._root.character == char:
                return bits
            else:
                return ""
        else:
            return self._left.find_huffman_value(char, bits + "0") + self._right.find_huffman_value(char, bits + "1")

def get_min(lst: list[tuple]) -> tuple:
    min_so_far = lst[0]
    for i in lst:
        if i[0] <= min_so_far[0]:
            min_so_far = i
    return min_so_far
