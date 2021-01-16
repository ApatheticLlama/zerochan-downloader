import os
import tkinter as tk
from tkinter import filedialog, OptionMenu

from linkgenerator import LinkGenerator
from pagereader import PageReader

class DownloaderGUI:
    def __init__(self):
        self.download_dir = os.getcwd() # default download location

        # tkinter stuff
        self.root = tk.Tk()
        self.root.title("Zerochan Downloader v0.0.1")
        self.option_list = ("Popular", "Recent", "Random")

        self.default_sort = tk.StringVar()
        self.default_sort.set("Popular")

        self.download_dir = tk.StringVar()
        self.download_dir.set(os.getcwd())

        self.frm_dir = tk.Frame()
        self.frm_download = tk.Frame()

        self.lbl_tags = tk.Label(text="Tags (Comma Separated)")
        self.lbl_count = tk.Label(text="Number of images")
        self.lbl_sort = tk.Label(text="Sort")

        self.ent_tags = tk.Entry()
        self.ent_count = tk.Entry()

        self.opt_sort = tk.OptionMenu(self.root, self.default_sort, *self.option_list) 

        self.btn_dir = tk.Button(text="Folder", command=self.get_dir, master=self.frm_dir)
        self.btn_dir.pack()

        self.btn_download = tk.Button(text="Download", command=self.download_images, master=self.frm_download)
        self.btn_download.pack()

        # i don't know how to do this in any better way
        self.lbl_tags.pack()
        self.ent_tags.pack()

        self.lbl_count.pack()
        self.ent_count.pack()

        self.lbl_sort.pack()
        self.opt_sort.pack()

        self.frm_dir.pack()
        self.frm_download.pack()


    def get_dir(self):
        self.download_dir = filedialog.askdirectory()

    def get_link(self):

        url = LinkGenerator(self.ent_tags.get(), self.ent_count.get(), self.opt_sort.get())
        link = url.generate_link()
        return link
    
    def download_images(self):
        pass

if __name__ == "__main__":
    bruh = DownloaderGUI()
    tk.mainloop()
    print(bruh.get_link())