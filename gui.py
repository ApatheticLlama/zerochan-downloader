import os
import tkinter as tk
from tkinter import filedialog, OptionMenu

from linkgenerator import LinkGenerator
from pagereader import PageReader

class DownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zerochan Downloader v0.0.1")
        self.option_list = ("Popular", "Recent", "Random")

        self.sort_method = tk.StringVar()
        self.sort_method.set("Popular")

        self.download_dir = tk.StringVar()
        self.download_dir.set(os.getcwd())

        self.lbl_tags = tk.Label(text="Tags (Comma Separated)") # labels
        self.lbl_count = tk.Label(text="Number of images")
        self.lbl_sort = tk.Label(text="Sort")

        self.ent_tags = tk.Entry() # entries
        self.ent_count = tk.Entry()

        self.opt_sort = tk.OptionMenu(self.root, self.sort_method, *self.option_list) 

        self.frm_dir = tk.Frame() # directory frame
        self.btn_dir = tk.Button(text="Folder", command=self.get_dir, master=self.frm_dir)
        self.btn_dir.pack(side=tk.LEFT)

        self.lbl_dir = tk.Label(textvariable=self.download_dir, master=self.frm_dir)
        self.lbl_dir.pack(side=tk.LEFT)

        self.frm_download = tk.Frame() # download frame
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
        self.download_dir.set(filedialog.askdirectory())

    def get_link(self):
        url = LinkGenerator(self.ent_tags.get(), self.sort_method.get())
        link = url.generate_link()
        return link
    
    def download_images(self):
        self.btn_download.configure(state=tk.DISABLED)
        link = self.get_link()
        pagereader = PageReader(link, int(self.ent_count.get()))
        pagereader.collect_links()  
        #pagereader.download()

if __name__ == "__main__":
    bruh = DownloaderGUI()
    tk.mainloop()
