"""This file is the main file for the text compressor.

This file is Copyright (c) 2023 Will Kukkamalla, Alex Lee, Kirill Logoveev, and Brandon Wong.
"""
from __future__ import annotations
from math import ceil
import codecs
from tkinter import *
from tkinter import ttk, filedialog
import shutil
import pandas as pd
from tree import Node, HuffmanTree

# Optional modules used for the tree visualization, which only works after downloading the library from the website.
# import graphviz
# import tree_visualization


def browse_file() -> str:
    """Function that allows the user to select a file
    """
    filename = filedialog.askopenfilename()
    return filename


def encode_ui() -> None:
    """Displays the GUI for encoding. Called when encode toggle button
    is clicked.
    """
    message = 'Enter the original text here...'
    new_label.config(text=message)
    view_label.config(text='Encoded text (view only)')
    # these buttons need their commands changed
    runner_button.config(text='Encode!', command=run_encode)
    download_file_button.config(text='Download Encoded File', command=download_encoded)
    input_text.delete(1, END)
    instruction_label.config(text='When using encode, the program will check whether or not the input text box has \n'
                                  'any text in it.\n\n'
                                  'If there is any text in the text box, then the encode function will run on the\n'
                                  'inputted text\n\n'
                                  'If there is no text in the text box, then you will have to choose a text file to \n'
                                  'encode. Note, that if you upload a file it MUST be a txt file. No other \n'
                                  'file type is supported\n\n'
                                  'When the encoding is finished, then there will be a prompt to download the key.\n\n'
                                  'Please note that you must download the encoded file via the Download '
                                  'Encoded File button.\n\n '
                                  'Note that you are required to download these files to decode.',
                             justify=LEFT)


def decode_ui() -> None:
    """Displays the GUI for decoding. Called when decode toggle button is clicked.
    """
    message = 'Enter the encoded text here...'
    new_label.config(text=message)
    view_label.config(text='Decoded text (view only)')
    # these buttons need their command changed
    runner_button.config(text='Decode!', command=run_decode)
    download_file_button.config(text='Download Decoded File', command=download_final_file)
    input_text.delete(1, END)
    instruction_label.config(text='When using decode, the program will check whether the input text box has text in it'
                                  '\n\nIf there is text, when pressing Decode!, you the first file you need to input is'
                                  '\n'
                                  'the CSV file for the key you got from encode then you can input the downloaded bnr '
                                  'file'
                                  '\n\n'
                                  'If you wish to decode text by using inputing text into the text box, then \n'
                                  'The first file you need to input is the key and the SECOND file you need to input\n'
                                  '\n'
                                  'is the encoded file you downloaded from encode\n\n'
                                  'Please note that you may also download the decoded file via the \n'
                                  'Download Decoded File button',
                             justify=LEFT)


def download_final_file() -> None:
    """When the user clicks the download decoded file this function is called and downloads that file"""
    original = r'output.txt'
    target = filedialog.asksaveasfile(defaultextension=".csv")

    shutil.copyfile(original, target.name)


def run_encode() -> None:
    """
    Runs the backend encode function given
    This will call encode_input or encode based off of whether there
    is any text in the input_text box

    This will display a pop up for the option to download the key
    """
    # this should return the encoded file, the SER file
    if len(input_text.get()) > 0:
        # save_text()
        do_this_str = input_text.get()
        encode_text = encode_input(do_this_str)
        view_box.delete(0, END)
        view_box.insert(0, encode_text)

    else:
        encoded_file = browse_file()
        encode(encoded_file)
    pop_up = Toplevel(root)
    pop_up.geometry("550x250")
    pop_up.title("Encode Finished")
    final_label = Label(pop_up, text="Your encode is finished! Please download the CSV file to be able to decode")
    final_label.pack()
    final_download = Button(pop_up, text='Download!', command=download_key)
    final_download.pack()


def save_text() -> None:
    """
    This function saves the text within input_text
    to the input.txt file

    This is used later for the encode and decode functons for inputed text
    """
    with open("input.txt", "w") as f:
        text_to_save = input_text.get(1, END)
        f.write(text_to_save)
        f.close()


def run_decode() -> None:
    """
    Runs the backend
    This will call decode_input or decode based off of whether there
    is any text in the input_text box
    """
    key = filedialog.askopenfilename()
    if len(input_text.get()) > 0:
        do_this_str = input_text.get()
        dis = decode_input(do_this_str, key)
        view_box.delete(0, END)
        view_box.insert(0, dis)
    else:
        decoded_file = browse_file()
        decode(decoded_file, key)

    pop_up = Toplevel(root)
    pop_up.geometry("550x250")
    pop_up.title("Decode Finished")
    final_label = Label(pop_up, text="Your decode has finished! You may close this window!")
    final_label.pack()


def download_key() -> None:
    """
    This method allows you to download the huffman key after decode or decode_input has run
    """
    original = r'key.csv'
    target = filedialog.asksaveasfile(defaultextension=".csv")

    shutil.copyfile(original, target.name)


def download_encoded() -> None:
    """
    This method allows you to download the encoded file after encode or encode_input has run
    """
    original = r'output.bnr'
    target = filedialog.asksaveasfile(defaultextension=".bnr")
    shutil.copyfile(original, target.name)


def open_file(file: str) -> dict:
    """Opens the file passed in and returns the characters and thier frequencies as a dicitonary
    """
    frequency = {}
    with codecs.open(file, encoding="utf-8") as f:
        lines = f.readlines()
        for i in lines:
            for j in i:
                if j not in frequency:
                    frequency[j] = 1
                else:
                    frequency[j] += 1
    return frequency


def get_binary_values(tree: HuffmanTree, letters: list) -> dict:
    """
    Given the tree and the letters it returns the a dictionary that maps the character to their binary value

    Preconditions:
        - tree is not None and isinstance(tree, HuffmanTree)
    """
    values = {}
    for i in letters:
        value = tree.find_huffman_value(i, "")
        values[i] = value
    return values


def encode_input(text: str) -> str:
    """
    Encodes the text that the user inputs
    Preconditions:
        - text is not None
    """
    # Creates a key by iterating though the string
    key = {}
    for i in text:
        if i in key:
            key[i] += 1
        else:
            key[i] = 1

    # Uses the key to create a Huffman Tree
    tree = HuffmanTree(1)
    key_list = []
    letters = []
    for i in key:
        key_list.append(Node(i, key[i]))
        letters.append(i)
    tree.add(key_list)

    # writes the binary output
    values = get_binary_values(tree, letters)
    output = ""
    for i in text:
        output += values[i]

    char = []
    freq = []
    for i in key_list:
        char.append(i.character)
        freq.append(i.frequency)

    df = pd.DataFrame({
        "Character": char,
        "Frequency": freq
    })
    df.to_csv("key.csv")

    return output


def encode(file: str) -> None:
    """Function that encodes and writes the new binary representations of characters to a .bnr file"""
    # Reads the file and returns a dictionary with all of the letters and their frequencies
    tree, letters, lst = create_tree_with_file(file)

    values = get_binary_values(tree, letters)

    bits_so_far = ""

    # Read through the input file
    with codecs.open(file, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            for character in line:
                # for every character, get their bitset, and set those numbers to the bits_out
                # Nuance: the bits_out are cast to be a Byte Array, and then it's written to the output file

                sequence_bits = values[character]

                bits_so_far += sequence_bits

            # Writes the encoded text to a bnr file for the user to download later
            with open("output.bnr", "wb") as o:
                o.write(int(bits_so_far[::-1], 2).to_bytes(ceil(len(bits_so_far) / 8), 'little'))

        # Creates the key for the user to download to later decode the file
        create_csv_key(lst)


def create_csv_key(lst: list) -> None:
    """Creates a csv file with the characters and their frequencies which will be used to decode the file"""
    char = []
    freq = []
    for i in lst:
        char.append(i.character)
        freq.append(i.frequency)

    df = pd.DataFrame({
        "Character": char,
        "Frequency": freq
    })
    df.to_csv("key.csv")


def create_tree_with_file(file: str) -> list:
    """Helper function for the encode funtion which creates the tree from the inputted file."""
    dictionary = open_file(file)

    letters = []
    # Creates the tree
    lst = []
    for i in dictionary:
        lst.append(Node(i, dictionary[i]))
        letters.append(i)
    tree = HuffmanTree(1)
    tree.add(lst)

    return [tree, letters, lst]


def decode_input(text: str, key: str) -> str:
    """
    Decodes from the input text box
    """
    # Creates the tree from the key file
    key_lst = []
    key_csv = pd.read_csv(key)
    for row in key_csv.iterrows():
        key_lst.append(Node(row["Character"], row["Frequency"]))

    # Creates the tree to decode the text
    tree = HuffmanTree(1)
    tree.add(key_lst)

    # Iterates through the input to return the decoded string
    output_so_far = ''
    string_so_far = ''
    for num in text:
        string_so_far += num

        char = tree.tree_find_character(string_so_far)

        if char is not None:
            output_so_far += char
            string_so_far = ""

    return output_so_far


def decode(file: str, key: str) -> str:
    """Decodes the given file by rebuilding the tree using the key"""
    tree = create_tree_with_key(key)

    # tree_visualization.tree_to_svg(tree, 0, set())

    # Opens the file to decode the text
    with open(file, "rb") as f:
        lines = f.readlines()

        # Iterates the throuh the file to get the bytes
        line_so_far = ""
        string_so_far = ""

        with open("output.txt", "w") as o:
            for line in lines:

                # Turns the byte into a string of either 0 or 1
                x = format(int.from_bytes(line, 'little'), '023b')[::-1]
                line = str(x)
                # iterates though every single one or zero
                for charater in line:
                    string_so_far = string_so_far + charater
                    char = tree.tree_find_character(string_so_far)

                    # if the char is found then it resets the string to find the next character
                    if char is not None:

                        # line_so_far = line_so_far + string_so_far
                        line_so_far += char
                        string_so_far = ""
                        o.write(char)
        return line_so_far


def create_tree_with_key(key: str) -> HuffmanTree:
    """Helper function for the decode function which creates the tree from the key."""
    key_lst = []
    key_csv = pd.read_csv(key)
    for i, row in key_csv.iterrows():
        key_lst.append(Node(row["Character"], row["Frequency"]))

    # Creates the tree to decode the text
    tree = HuffmanTree(1)
    tree.add(key_lst)

    return tree


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    root = Tk()
    root.geometry('1400x900')
    root.title('File Compressor')

    # creating new tabs
    tab_control = ttk.Notebook(root)
    tab1 = Frame(tab_control)
    tab2 = Frame(tab_control)
    tab_control.add(tab1, text='Encode or Decode')
    tab_control.add(tab2, text='Tree Visualization')
    tab_control.pack(expand=1, fill='both')

    new_label = Label(tab1, text='Please select an option')
    new_label.place(x=20, y=20, anchor='w')

    input_text = Entry(tab1)
    input_text.place(x=20, y=40, width=750, height=350)

    view_label = Label(tab1, text='Please select an option')
    view_label.place(x=20, y=410, anchor='w')

    view_box = Entry(tab1)
    view_box.place(x=20, y=430, width=750, height=350)
    # view_box.config(state=DISABLED)

    # Toggle buttons
    var = IntVar(None, 1)  # '1' represents the default toggle option
    run_var = IntVar(None, 1)
    encode_button = Radiobutton(tab1, text='Encode', command=encode_ui, variable=var, value=1)
    encode_button.place(x=1000, y=20)
    decode_button = Radiobutton(tab1, text='Decode', command=decode_ui, variable=var, value=2)
    decode_button.place(x=1100, y=20)

    runner_button = Button(tab1, text='', width=30, height=5, command=run_encode)
    runner_button.place(x=1250, y=150, anchor='e')

    download_file_button = Button(tab1, text='Download Encoded File', width=30, height=5, command=download_key)
    download_file_button.place(x=1250, y=250, anchor='e')

    instruction_label = Label(tab1, text='Instructions')
    instruction_label.place(x=900, y=450, anchor='w')
    encode_ui()

    root.mainloop()

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'typing', "tree", "math", "codecs", "struct", "tkinter", "pandas",
                          "shutil", "graphviz", 'tree_visualization'],
        'disable': ["too-many-function-args", "forbidden-import", "wildcard-import"],
        'allowed-io': ['encode', 'decode', 'open_file', "save_text", "create_csv_key", "create_tree_with_file"]
    })
