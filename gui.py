import tkinter as tk
from tkinter import filedialog, OptionMenu

class DownloaderGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zerochan Downloader" +  version)

        self.option_list = ("Popular", "Recent", "Random")
        self.v = tk.StringVar()
        self.v.set("Popular")

        self.lbl_tags = tk.Label(text="Tags (Comma Separated)")
        self.lbl_count = tk.label(text="Number of Pages to Parse")
        self.lbl_sort = tk.label(text="Sort Method")

        self.ent_tags = tk.Entry()
        self.ent_count = tk.Entry()
        self.opt_sort = tk.OptionMenu(self.root, self.v, *self.option_list) 

        self.btn_dir = tk.Button(text="Folder", command=self.get_dir)

        # i don't know how to do this in any better way
        self.lbl_tags.pack()
        self.ent_tags.pack()

        self.lbl_count.pack()
        self.ent_count.pack()

        self.lbl_sort.pack()
        self.opt_sort.pack()

        self.btn_dir.pack()

    def get_dir(self):
        filedialog.askdirectory()