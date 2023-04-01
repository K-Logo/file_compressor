"""
This file is the main file for the text compressor
"""
from __future__ import annotations
from tree import Node, HuffmanTree
from math import ceil
import codecs
import struct
from typing import Any
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import shutil
#import tree_visualization
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk


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
    download_file_button.config(text='Download Encoded File', command=downloadEncoded)

    # runner_button_for_text.config(text='Run Encode for Text!!', command = run_encode)
    input_text.delete(1, END)

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
    download_file_button.config(text='Download Decoded File', command=download_final_file)
    input_text.delete(1, END)

    # runner_button_for_text.config(text='DO NOT CLICK')
    return None

def download_final_file() -> None:
    original = r'output.txt'
    target = filedialog.asksaveasfile(defaultextension=".csv")
    print("Saved to" + target.name)
    shutil.copyfile(original, target.name)

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
    Should be connected to a back end function
    """
    # this should return the encoded file, the SER file
    if len(input_text.get()) > 0:
        # save_text()
        do_this_str = input_text.get()
        encode_text = encode_input(do_this_str)


        view_box.delete(0, END)
        view_box.insert(0, encode_text)
        print("Encode UI done!")
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
   text_file.write(input_text.get(1, END))
   text_file.close()


def run_decode() -> None:
    """
    Runs the backend
    Should be connected to a back end funtion
    """
    key = filedialog.askopenfilename()
    if len(input_text.get()) > 0:
        do_this_str = input_text.get()
        display = decode_input(do_this_str, key)
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
    target = filedialog.asksaveasfile(defaultextension=".bnr")
    print("Saved to" + target.name)
    shutil.copyfile(original, target.name)


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
                    frequency[j] = 1
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

def encode_input(text: str) -> str:
    """
    Encodes the text that the user inputs
    """
    # Creates a key by iterating though the string
    key = dict()
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

    #
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
    print("Encoding Done!")

    return output




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
        print("Encoding Done!")


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
        return line_so_far

def get_svg(svg_file: str) -> None:
    """Fetch the svg file, and save a file called treegraph.png

    Preconditions:
        - svg_file is a valid file name of a csv file in the same directory
    """
    image = svg2rlg(svg_file)
    renderPM.drawToFile(image, "treegraph.png", fmt="PNG", dpi=200)

# class AutoScrollbar(ttk.Scrollbar):
#     ''' A scrollbar that hides itself if it's not needed.
#         Works only if you use the grid geometry manager '''
#     def set(self, lo, hi):
#         if float(lo) <= 0.0 and float(hi) >= 1.0:
#             self.grid_remove()
#         else:
#             self.grid()
#             ttk.Scrollbar.set(self, lo, hi)
#
#     def pack(self, **kw):
#         raise tk.TclError('Cannot use pack with this widget')
#
#     def place(self, **kw):
#         raise tk.TclError('Cannot use place with this widget')
#
# class Zoom_Advanced(ttk.Frame):
#     ''' Advanced zoom of the image '''
#     def __init__(self, mainframe, path):
#         ''' Initialize the main Frame '''
#         ttk.Frame.__init__(self, master=mainframe)
#         # Vertical and horizontal scrollbars for canvas
#         vbar = AutoScrollbar(self.master, orient='vertical')
#         hbar = AutoScrollbar(self.master, orient='horizontal')
#         vbar.grid(row=0, column=1, sticky='ns')
#         hbar.grid(row=1, column=0, sticky='we')
#         # Create canvas and put image on it
#         self.canvas = tk.Canvas(self.master, highlightthickness=0,
#                                 xscrollcommand=hbar.set, yscrollcommand=vbar.set)
#         self.canvas.grid(row=0, column=0, sticky='nswe')
#         self.canvas.update()  # wait till canvas is created
#         vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
#         hbar.configure(command=self.scroll_x)
#         # Make the canvas expandable
#         self.master.rowconfigure(0, weight=1)
#         self.master.columnconfigure(0, weight=1)
#         # Bind events to the Canvas
#         self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
#         self.canvas.bind('<ButtonPress-1>', self.move_from)
#         self.canvas.bind('<B1-Motion>',     self.move_to)
#         self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
#         self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
#         self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
#         self.image = Image.open(path)  # open image
#         self.width, self.height = self.image.size
#         self.imscale = 1.0  # scale for the canvaas image
#         self.delta = 1.3  # zoom magnitude
#         self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
#         self.show_image()
#
#     def scroll_y(self, *args, **kwargs):
#         ''' Scroll canvas vertically and redraw the image '''
#         self.canvas.yview(*args, **kwargs)  # scroll vertically
#         self.show_image()  # redraw the image
#
#     def scroll_x(self, *args, **kwargs):
#         ''' Scroll canvas horizontally and redraw the image '''
#         self.canvas.xview(*args, **kwargs)  # scroll horizontally
#         self.show_image()  # redraw the image
#
#     def move_from(self, event):
#         ''' Remember previous coordinates for scrolling with the mouse '''
#         self.canvas.scan_mark(event.x, event.y)
#
#     def move_to(self, event):
#         ''' Drag (move) canvas to the new position '''
#         self.canvas.scan_dragto(event.x, event.y, gain=1)
#         self.show_image()  # redraw the image
#
#     def wheel(self, event):
#         ''' Zoom with mouse wheel '''
#         x = self.canvas.canvasx(event.x)
#         y = self.canvas.canvasy(event.y)
#         bbox = self.canvas.bbox(self.container)  # get image area
#         if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
#         else: return  # zoom only inside image area
#         scale = 1.0
#         # Respond to Linux (event.num) or Windows (event.delta) wheel event
#         if event.num == 5 or event.delta == -120:  # scroll down
#             i = min(self.width, self.height)
#             if int(i * self.imscale) < 30: return  # image is less than 30 pixels
#             self.imscale /= self.delta
#             scale        /= self.delta
#         if event.num == 4 or event.delta == 120:  # scroll up
#             i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
#             if i < self.imscale: return  # 1 pixel is bigger than the visible area
#             self.imscale *= self.delta
#             scale        *= self.delta
#         self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
#         self.show_image()
#
#     def show_image(self, event=None):
#         ''' Show image on the Canvas '''
#         bbox1 = self.canvas.bbox(self.container)  # get image area
#         # Remove 1 pixel shift at the sides of the bbox1
#         bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
#         bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
#                  self.canvas.canvasy(0),
#                  self.canvas.canvasx(self.canvas.winfo_width()),
#                  self.canvas.canvasy(self.canvas.winfo_height()))
#         bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
#                 max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
#         if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
#             bbox[0] = bbox1[0]
#             bbox[2] = bbox1[2]
#         if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
#             bbox[1] = bbox1[1]
#             bbox[3] = bbox1[3]
#         self.canvas.configure(scrollregion=bbox)  # set scroll region
#         x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
#         y1 = max(bbox2[1] - bbox1[1], 0)
#         x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
#         y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
#         if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
#             x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
#             y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
#             image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
#             imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
#             imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
#                                                anchor='nw', image=imagetk)
#             self.canvas.lower(imageid)  # set image into background
#             self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection


# Below is the code for the scroll bar and zooming/dragging into the tree graph
# Code source: https://stackoverflow.com/questions/25787523/move-and-zoom-a-tkinter-canvas-with-mouse/48069295#48069295
class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')


class Zoom(ttk.Frame):
    ''' Simple zoom with mouse wheel '''
    def __init__(self, mainframe, path):
        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Open image
        self.image = Image.open(path)
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        vbar.configure(command=self.canvas.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.canvas.xview)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        # Show image and plot some random test rectangles on the canvas
        self.imscale = 1.0
        self.imageid = None
        self.delta = 0.75
        # Text is used to set proper coordinates to the image. You can make it invisible.
        self.text = self.canvas.create_text(0, 0, anchor='nw', text='Scroll to zoom')
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            scale        *= self.delta
            self.imscale *= self.delta
        if event.num == 4 or event.delta == 120:
            scale        /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def show_image(self):
        ''' Show image on the Canvas '''
        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None  # delete previous image from the canvas
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(self.canvas.coords(self.text),
                                                anchor='nw', image=imagetk)
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    get_svg("treegraph.svg")  # Convert svg file to png

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

    # Loading the tree graph image (tab2)

    zoomy = Zoom(tab2, 'treegraph.png')
    # img = Image.open('treegraph.png')
    #
    # photo_image = ImageTk.PhotoImage(img)
    #
    # tree_graph = Label(tab2, image=photo_image)
    # tree_graph.pack()



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
