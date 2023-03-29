"""
This file is the main file for the text compressor
"""
from __future__ import annotations
from tree import Node, HuffmanTree
from math import ceil
import codecs
import struct
from typing import Any
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import shutil
#import tree_visualization


def browse_tree() -> None:
    """Function that allows the user to select a file that is the tree, used when decoding"""
    filename = filedialog.askopenfilename()
    tree_file = filename


def browse_encode() -> str:
    """Function that allows the user to select a file to encode"""
    filename = filedialog.askopenfilename()
    return filename


def browse_decode() -> str:
    """Function that allows the user to select a file to decode"""
    decode_file = filedialog.askopenfilename()
    return decode_file


def input_key(key: str) -> list:
    """
    >>> input_key("a5c3")

    """
    # do something so it gets the string from the input box
    key_so_far = []
    for i in range(len(key) - 1):
        if i % 2 == 0:
            char = key[i]
            freq = key[i + 1]
            key_so_far.append(Node(char, freq))
    return key_so_far


def encode_ui() -> None:
    """
    Displays the GUI for encoding. Called when encode toggle button
    is clicked.
    """
    message = 'Enter the original text here...'
    new_label.config(text=message)
    view_label.config(text='Encoded text (view only)')

    # these buttons need their commands changed
    runner_button.config(text='Encode!', command=run_encode)
    # upload_file_button.config(command=browse_encode)
    # huffman_tree_button.config(text='Download Huffman Tree', command=download)
    download_file_button.config(text='Download Encoded File and Tree')

    # runner_button_for_text.config(text='Run Encode for Text!!', command = run_encode)

    return None


def decode_ui() -> None:
    """
    Displays the GUI for decoding. Called when decode toggle button
    is clicked.
    """
    message = 'Enter the encoded text here...'
    new_label.config(text=message)
    view_label.config(text='Decoded text (view only)')

    # these buttons need their command changed
    runner_button.config(text='Decode!', command=run_decode)
    # upload_file_button.config(command=browse_decode)
    # huffman_tree_button.config(text='Upload Huffman Tree', command=browse_tree)
    download_file_button.config(text='Download Decoded File')

    # runner_button_for_text.config(text='DO NOT CLICK')
    return None

# def run_encode_for_text() -> None:
#     save_text()
#     encode('input.txt')
#
#     pop_up = Toplevel(root)
#     pop_up.geometry("550x250")
#     pop_up.title("Encode Finished")
#     final_label = Label(pop_up, text="Your encode is finished! Please download the CSV file to be able to decode")
#     final_label.pack()
#     final_download = Button(pop_up, text='Download!', command=downloadKey)
#     final_download.pack()

def run_encode() -> None:
    """
    Runs the backend
    Should be connected to a back end funtion
    """
    # this should return the encoded file, the SER file
    if len(input_text.get(1.0, END)) >= 1:
        save_text()
        encode('input.txt')

    else:
        encoded_file = browse_encode()
        encode(encoded_file)

    pop_up = Toplevel(root)
    pop_up.geometry("550x250")
    pop_up.title("Encode Finished")
    final_label = Label(pop_up, text="Your encode is finished! Please download the CSV file to be able to decode")
    final_label.pack()
    final_download = Button(pop_up, text='Download!', command=downloadKey)
    final_download.pack()

    encode_text =""
    with open("output.bnr", "rb") as f:
        lines = f.readlines()

        for line in lines:
            x = format(int.from_bytes(line, 'little'), '023b')[::-1]
            line = str(x)
            for char in line:
                encode_text = encode_text + str(char)

    print(encode_text)
    view_box.delete(0, END)
    view_box.insert(0, encode_text)
    # display_string = 'Paste this into the pop up for decode to decode your file!: '
    #
    # key_label = Text(tab1, height=50)
    # key_label.place(x=1000, y=400, anchor='center')
    # key_label.insert(INSERT, display_string)
    # key_label.config(state=False)
    # key_label.pack()

    # and the Huffman tree for visualzation
    #tree_visualization.tree_visualization(...)

    # img = Label(tab2, image='graph.png')
    # # tkimage = Image.PhotoImage(img)
    # # final_image = Label(tab2, image=tkimage)
    # # final_image.pack()
    # img.place(x=0, y=0, anchor='center')

def save_text():
   text_file = open("input.txt", "w")
   text_file.write(input_text.get(1.0, END))
   text_file.close()


def run_decode() -> None:
    """
    Runs the backend
    Should be connected to a back end funtion
    """
    key = filedialog.askopenfilename()
    if len(input_text.get(1.0, END)) >= 1:
        display = decode_input(input_text.get(1.0, END), key)
    else:
        decoded_file = browse_decode()
        display = decode(decoded_file, key)

    # Get input for key

    view_box.delete(0, END)
    view_box.insert(0, display)


def downloadKey() -> None:
    """
    This method allows you to download certain files that are outputted
    This should call the backend methods and return something
    The return type of None should be changed later
    """
    original = r'key.csv'
    target = filedialog.asksaveasfile(defaultextension=".csv")
    print("Saved to" + target.name)
    shutil.copyfile(original, target.name)

def downloadEncoded() -> None:
    """
    This method allows you to download certain files that are outputted
    This should call the backend methods and return something
    The return type of None should be changed later
    """

    original = r'output.bnr'
    target = filedialog.askopenfilename()


    shutil.copyfile(original, target)


def open_file(file: str) -> dict:
    """
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


def get_binary_values(tree, letters) -> dict:
    """Returns a dict"""
    values = {}
    for i in letters:
        value = tree.find_huffman_value(i, "")
        values[i] = value
    return values


def encode(file: str):
    """Function that encodes and writes the new binary representations of characters to a .bnr file"""
    # Reads the file and returns a dictionary with all of the letters and their frequencies
    dict = open_file(file)
    letters = []
    # Creates the tree
    lst = []
    for i in dict:
        lst.append(Node(i, dict[i]))
        letters.append(i)
    tree = HuffmanTree(1)
    tree.add(lst)

    values = get_binary_values(tree, letters)

    string = ""

    # Read through the input file
    with codecs.open(file, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            for character in line:
                # for every character, get their bitset, and set those numbers to the bits_out
                # Nuance: the bits_out are cast to be a Byte Array, and then it's written to the output file

                sequence_bits = values[character]

                string += sequence_bits

            with open("output.bnr", "wb") as o:
                o.write(int(string[::-1], 2).to_bytes(ceil(len(string) / 8), 'little'))

        char = []
        freq = []
        for i in lst:
            char.append(i.character)
            freq.append(i.frequency)

        df = pd.DataFrame({
            "Character":char,
            "Frequency":freq
        })
        df.to_csv("key.csv")


def decode_input(input: str, key: str) -> str:
    """"Decodes from the input text box"""

    # Creates the tree from the key file
    key_lst = []
    key_csv = pd.read_csv(key)
    for i, row in key_csv.iterrows():
        key_lst.append(Node(row["Character"], row["Frequency"]))

    # Creates the tree to decode the text
    tree = HuffmanTree(1)
    tree.add(key_lst)

    # Iterates through the input to return the decoded string
    output_so_far = ''
    string_so_far = ''
    for num in input:
        string_so_far += num

        char = tree.find_character(string_so_far)

        if char is not None:
            output_so_far += char
            string_so_far = ""

    return output_so_far

def decode(file: str, key: str) -> str:
    """Decodes the given file by rebuilding the tree using the key"""
    key_lst = []
    key_csv = pd.read_csv(key)
    for i, row in key_csv.iterrows():
        key_lst.append(Node(row["Character"], row["Frequency"]))
    # Creates the tree to decode the text
    tree = HuffmanTree(1)
    tree.add(key_lst)

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
                print(line)
                # iterates though every single one or zero
                for charater in line:
                    string_so_far = string_so_far + charater
                    char = tree.find_character(string_so_far)

                    # if the char is found then it resets the string to find the next character
                    if char is not None:

                        # line_so_far = line_so_far + string_so_far
                        line_so_far += char
                        string_so_far = ""
                        o.write(char)
        print(line_so_far)
        return line_so_far


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

    input_text = Text(tab1)
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

    # runner_button_for_text = Button(tab1, text='', width=30, height=5, command=run_encode)
    # runner_button_for_text.place(x=1250, y=250, anchor='e')

    # upload_file_button = Button(tab1, text='Upload Text File...', command=browse_encode, width=30, height=5)
    # upload_file_button.place(x=1250, y=350, anchor='e')
    #
    # huffman_tree_button = Button(tab1, text='', command=browse_tree, width=30, height=5)
    # huffman_tree_button.place(x=1250, y=450, anchor='e')
    #
    download_file_button = Button(tab1, text='Download Encoded File', width=30, height=5, command=downloadKey)
    download_file_button.place(x=1250, y=550, anchor='e')
    encode_ui()

    root.mainloop()

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
