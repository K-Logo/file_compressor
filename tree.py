from typing import Any, Optional
# from Bitset import Bitset


class Node:
    """Class for the Node data type."""
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

    def find_character(self, bit: str) -> str:
        return self.character


class HuffmanTree:
    """Contains the code for the huffman tree"""
    _root: Optional[Node]

    def __init__(self, root: Optional[Node] | Optional[int]) -> None:
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = HuffmanTree(None)
            self._right = HuffmanTree(None)

    def add_subtrees(self, left: Optional[Node], right: Optional[Node]):
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

            tree = HuffmanTree(root=min1_num[0] + min2_num[0])

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
            self._right = HuffmanTree(node)

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

    def find_character(self, bits: str) -> Optional[str]:
        """
        >>> tree = HuffmanTree(1)
        >>> tree.add([Node("c", 1), Node("a", 2),Node("b", 8),Node("d", 6),Node("g", 5),])
        >>> tree.find_character(bits="0011")

        :param bits:
        :return:
        """
        if self._left is None and self._right is None:
            return self._root.character
        elif len(bits) == 0:
            return None
        elif bits[0] == '1':
            bits = bits[1:]
            return self._right.find_character(bits)
        elif bits[0] == "0":
            bits = bits[1:]
            return self._left.find_character(bits)

    def get_root_frequency(self) -> int:
        if isinstance(self._root, int):
            return self._root
        else:
            return self._root.frequency

    def get_edges_and_verticies(self, final_verticies: [], final_edges: []) -> None:
        """
        Recursively mutate final_verticies and final_edges

        >>> tree = HuffmanTree(1)
        >>> tree.add([Node("c", 1), Node("a", 2),Node("b", 8),Node("d", 6),Node("g", 5),])
        >>> lst = []
        >>> edges = []
        >>> tree.get_edges_and_verticies(lst, edges)
        >>> lst
        >>> edges
        """
        instant_vertices_dict = {}
        instant_vertices_dict['frequency'] = self.get_root_frequency()
        instant_vertices_dict['character'] = ''

        if self._right is not None:
            instant_edges_dict = {}
            instant_edges_dict['source'] = self.get_root_frequency()

            if isinstance(self._right, HuffmanTree):
                instant_edges_dict['target'] = self._right.get_root_frequency()

            elif isinstance(self._right, Node):
                instant_edges_dict['target'] = self._right.frequency
                node_vertices_dict = {}
                node_vertices_dict['frequency'] = self._right.frequency
                node_vertices_dict['character'] = self._right.character
                final_verticies.append(node_vertices_dict)

            instant_edges_dict['bit'] = 1
            final_edges.append(instant_edges_dict)

            if isinstance(self._right, HuffmanTree):
                self._right.get_edges_and_verticies(final_verticies, final_edges)

        if self._left is not None:
            instant_edges_dict = {}
            instant_edges_dict['source'] = self.get_root_frequency()

            if isinstance(self._left, HuffmanTree):
                instant_edges_dict['target'] = self._left.get_root_frequency()

            elif isinstance(self._left, Node):
                instant_edges_dict['target'] = self._left.frequency
                node_vertices_dict = {}
                node_vertices_dict['frequency'] = self._left.frequency
                node_vertices_dict['character'] = self._left.character
                final_verticies.append(node_vertices_dict)

            instant_edges_dict['bit'] = 0
            final_edges.append(instant_edges_dict)

            if isinstance(self._left, HuffmanTree):
                self._left.get_edges_and_verticies(final_verticies, final_edges)

        final_verticies.append(instant_vertices_dict)


def get_min(lst: list[tuple]) -> tuple:
    min_so_far = lst[0]
    for i in lst:
        if i[0] <= min_so_far[0]:
            min_so_far = i
    return min_so_far
