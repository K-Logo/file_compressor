from __future__ import annotations
from typing import Any
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tree_visualization

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

#################################################
# tab1/encode and decode
#################################################

new_label = Label(tab1, text = 'Please select an option')
new_label.place(x=20, y=20, anchor = 'w')

input_text = Text(tab1)
input_text.place(x=20, y=40, width=750, height=350)

view_label = Label(tab1, text = 'Please select an option')
view_label.place(x = 20, y = 410, anchor = 'w')

view_box = Text(tab1)
view_box.place(x=20, y=430, width=750, height=350)
view_box.config(state=DISABLED)

tree_file = ''
encode_file = ''
decode_file = ''


def browse_tree() -> None:
    filename = filedialog.askopenfilename()
    tree_file = filename


def browse_encode() -> None:
    filename = filedialog.askopenfilename()
    encode_file = filename


def browse_decode() -> None:
    decode_file = filedialog.askopenfilename()


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
    upload_file_button.config(command=browse_encode)
    huffman_tree_button.config(text='Download Huffman Tree', command=download)
    download_file_button.config(text='Download Encoded File and Tree')

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
    upload_file_button.config(command=browse_decode)
    huffman_tree_button.config(text='Upload Huffman Tree', command=browse_tree)
    download_file_button.config(text='Download Decoded File')
    return None


def run_encode() -> None:
    """
    Runs the backend
    Should be connected to a back end funtion
    """
    # this should return the encoded file, the SER file
    # and the Huffman tree for visualzation
    tree_visualization.tree_visualization(...)

    img = Label(tab2, image='graph.png')
    # tkimage = Image.PhotoImage(img)
    # final_image = Label(tab2, image=tkimage)
    # final_image.pack()
    img.place(x=0, y=0, anchor='center')


def run_decode() -> None:
    """
    Runs the backend
    Should be connected to a back end funtion
    """
    ...


def download() -> None:
    """
    This method allows you to download certain files that are outputted
    This should call the backend methods and return something
    The return type of None should be changed later
    """
    ...


# Toggle buttons
var = IntVar(None, 1)  # '1' represents the default toggle option
run_var = IntVar(None, 1)
encode_button = Radiobutton(tab1, text = 'Encode', command = encode_ui, variable=var, value = 1)
encode_button.place(x = 1000, y = 20)
decode_button = Radiobutton(tab1, text = 'Decode', command = decode_ui, variable=var, value = 2)
decode_button.place(x = 1100, y = 20)

runner_button = Button(tab1, text = '', width = 30, height=5, command = run_encode)
runner_button.place(x = 1250, y =150, anchor = 'e')

upload_file_button = Button(tab1, text = 'Upload Text File...', command=browse_encode, width = 30, height=5)
upload_file_button.place(x=1250, y=350, anchor = 'e')

huffman_tree_button = Button(tab1, text = '', command = browse_tree, width = 30, height=5)
huffman_tree_button.place(x=1250, y=450, anchor='e')

download_file_button = Button(tab1, text = '', width=30, height=5, command=download)
download_file_button.place(x=1250, y=550, anchor='e')
encode_ui()


########################################################################################
#tab2 AKA tree visulization
########################################################################################


# def helloCallBack():
#    myLabel = Label(tab2, text='hi')
# #    myLabel.place(x=500, y=100)
#    myLabel.pack()

# button = Button(tab1, text='help me', command=helloCallBack)
# button.place(relx = 0.6, rely = 0.6, anchor = 'center')

# myLabel = Label(tab2, text='hi')
# myLabel.place(relx = 0.5, rely = 0.5, anchor = 'center')

# Label_middle = Label(tab2,
#                         text ='Middle')
# Label_middle.place(relx = 0.4,
#                    rely = 0.4,
#                    anchor = 'center')

# # Textbox
# inputText = Text(tab1, height = 5, width = 20)
# inputText.pack()

# # Creating a label widget
# myLabel = Label(root, text='DAVID IS COOL')

# # Shoving it onto the screen
# # makes it as big as the labels that are being showed
# myLabel.pack()

root.mainloop()
