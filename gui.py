import os
import threading
import queue
import tkinter as tk
from tkinter import filedialog, OptionMenu

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

    def process_queue(self):
        try:
            data = self.thread_queue.get(False)
            flag = data[0]
            count = data[1:]

            if flag == 'b': #begin
                self.lbl_download.config(text=f"Fetching base url")
            elif flag == 'c': # collecting
                self.lbl_download.config(text=f"Collected {count} links")
            elif flag == 'd': # downloading
                self.lbl_download.config(text=f"Downloaded {count} images")
            else:
                self.lbl_download.config(text=f"No download in progress")
                self.btn_download.config(state=tk.NORMAL)
                return
        
        except queue.Empty:
            pass

        self.root.after(100, self.process_queue)
    
    def download_images(self):
        if not self.ent_count.get().isdigit() or not self.ent_tags.get() or not self.var_download_dir.get():
            return

        self.btn_download.configure(state=tk.DISABLED)

        pagereader = PageReader(self.var_download_dir.get(), int(self.ent_count.get()), self.ent_tags.get(), self.sort_method.get())

        download_thread = threading.Thread(target=pagereader.download, args=(self.thread_queue,)) # run it again that comma should have fixed it
        download_thread.setDaemon(True)
        download_thread.start()

        self.process_queue()

if __name__ == "__main__":
    bruh = DownloaderGUI()
    tk.mainloop()
