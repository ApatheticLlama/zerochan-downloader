import os
import threading
import queue
import tkinter as tk
from tkinter import filedialog, OptionMenu

from linkgenerator import LinkGenerator
from pagereader import PageReader

class DownloaderGUI():
    def __init__(self):
        # threading
        self.thread_queue = queue.Queue()

        # tk
        self.root = tk.Tk()
        self.root.title("Zerochan Downloader v0.0.1")
        self.option_list = ("Popular", "Recent", "Random")

        self.sort_method = tk.StringVar()
        self.sort_method.set("Popular")

        self.var_download_dir = tk.StringVar()
        self.var_download_dir.set(os.getcwd())

        self.lbl_tags = tk.Label(text="Tags (Comma Separated)") # labels
        self.lbl_count = tk.Label(text="Number of images")
        self.lbl_sort = tk.Label(text="Sort")

        self.ent_tags = tk.Entry() # entries
        self.ent_count = tk.Entry()

        self.opt_sort = tk.OptionMenu(self.root, self.sort_method, *self.option_list) 

        self.frm_dir = tk.Frame() # directory frame
        self.btn_dir = tk.Button(text="Folder", command=self.get_dir, master=self.frm_dir)
        self.btn_dir.pack(side=tk.LEFT)

        self.lbl_dir = tk.Label(textvariable=self.var_download_dir, master=self.frm_dir)
        self.lbl_dir.pack(side=tk.LEFT)

        self.frm_download = tk.Frame() # download frame
        self.btn_download = tk.Button(text="Download", command=self.download_images, master=self.frm_download)
        self.btn_download.pack(side=tk.LEFT)

        self.lbl_download = tk.Label(text="No download in progress", master=self.frm_download)
        self.lbl_download.pack(side=tk.LEFT)

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
        self.var_download_dir.set(filedialog.askdirectory())

    def get_link(self):
        url = LinkGenerator(self.ent_tags.get(), self.sort_method.get())
        link = url.generate_link()
        return link
    
    def process_queue(self):
        try:
            link_count = self.thread_queue.get(False)
            if link_count == "complete":
                print("complete")
                self.btn_download.configure(state=tk.NORMAL)
                return
            print(link_count)
        except queue.Empty:
            pass
        
        self.root.after(100, self.process_queue)

    def download_images(self):
        if not self.ent_count.get().isdigit() or not self.ent_tags.get() or not self.var_download_dir.get():
            return

        self.btn_download.configure(state=tk.DISABLED)

        link = self.get_link()
        pagereader = PageReader(link, self.var_download_dir.get(), int(self.ent_count.get()))

        download_thread = threading.Thread(target=pagereader.download, args=(self.thread_queue,))
        download_thread.start()

        self.process_queue()

        """
        
        self.lbl_download.config(text=f"Collecting Links (0/{self.ent_count.get()})")
        self.root.update()

        gen = pagereader.collect_links()

        while True:
            try:
                link_cnt = next(gen)
                self.lbl_download.config(text=f"Collecting Links ({min(link_cnt, int(self.ent_count.get()))}/{self.ent_count.get()})")
                self.root.update()
            except StopIteration:
                break

        self.lbl_download.config(text="Downloading Images (0/0)")
        self.root.update()

        gen = pagereader.download(self.var_download_dir)
        
        while True:
            try:
                img_downloaded = next(gen)
                self.lbl_download.config(text=f"Downloading Images ({img_downloaded}/{self.ent_count.get()})")
                self.root.update()
            except StopIteration:
                break
        
        self.lbl_download.config(text="No download in progress")
        self.btn_download.configure(state=tk.NORMAL)
        """

if __name__ == "__main__":
    bruh = DownloaderGUI()
    tk.mainloop()
