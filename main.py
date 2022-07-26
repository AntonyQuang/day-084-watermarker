from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from PIL import Image
import os

# -------- UI SETUP -------- #

root = Tk()
root.title("Watermarker")
root.geometry("600x600+0+0")
root_style = Style()

watermark_img = Image.open("watermark.png")


class FileManager:
    def __init__(self):
        self.browse_btn = Button(root, text="Browse image...", command=self.open_file)
        self.browse_btn.grid(row=0, column=0)

        self.watermark_btn = Button(root, text="Add Watermark")
        self.watermark_btn.grid(row=0, column=2)

        self.save_btn = Button(root, text="Save image", command=self.print_file)
        self.save_btn.grid(row=2, column=2)

        self.file = None
        self.image = None

    def open_file(self):
        filetypes = [('JPEG', '*.jpg')]
        self.file = filedialog.askopenfilename(title='Open an image',
                                               initialdir='/',
                                               filetypes=filetypes)

        messagebox.showinfo(title="Selected Image", message=self.file)
        self.image = Image.open(self.file)

    def print_file(self):
        if self.file:
            print(self.file)
        else:
            messagebox.showerror(title="No Image Selected", message="Please select a file first")


buttons = FileManager()

root.mainloop()
