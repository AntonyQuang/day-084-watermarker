from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from PIL import Image, ImageTk
import sv_ttk
import copy

# -------- UI SETUP -------- #

root = Tk()
sv_ttk.use_dark_theme()
root.title("Watermarker")
root.geometry("600x700+0+0")
root.config(padx=50, pady=50)

watermark_img = Image.open("watermark.png")

canvas = Canvas(width=500, height=500)
canvas_text = canvas.create_text(250, 250, text="Image will be previewed here", fill="white",
                                font=("Calibri", 12, "bold"))
canvas.grid(row=1, column=0, columnspan=3, pady=20)


# --------- LOGIC ---------- #

class FileManager:
    def __init__(self):
        # ----------- BUTTONS ---------------- #
        self.browse_btn = Button(root, text="Browse image...", command=self.open_file)
        self.browse_btn.grid(row=0, column=0, sticky="w")

        self.watermark_btn = Button(root, text="Add Watermark", command=self.add_watermark)
        self.watermark_btn.grid(row=0, column=2, sticky="e")

        self.quit_btn = Button(root, text="Quit", command=root.destroy)
        self.quit_btn.grid(row=2, column=0, sticky="w")

        self.save_btn = Button(root, text="Save image", command=self.save_file)
        self.save_btn.grid(row=2, column=2, sticky="e")

        self.file = None
        self.image = None
        self.merged_image = None

        self.filetypes = [('All image files', ('*.jpg', '*.jpeg', '*.jpe', '*.jfif', '*.gif', '*png', '*.bmp', '*.dib',
                                               '*tif', '*.tiff', '*.heic')),
                          ('JPEG', ('*.jpg', '*.jpeg', '*.jpe', '*.jfif')),
                          ('GIF', '*.gif'),
                          ('PNG', '*png'),
                          ('Bitmap', ('*.bmp', '*.dib')),
                          ('TIFF', ('*tif', '*.tiff')),
                          ('HEIC', '*.heic')
                          ]

    def open_file(self):
        self.file = filedialog.askopenfilename(title='Open an image',
                                               initialdir='/',
                                               filetypes=self.filetypes)
        if self.file:
            self.image = Image.open(self.file)
            self.image.thumbnail((500, 500))
            preview_img = ImageTk.PhotoImage(self.image)
            # Next line is to prevent the image garbage collected when the function ends
            root.preview_img = preview_img
            canvas_image = canvas.create_image(250, 250, image=preview_img)
            canvas.itemconfig(canvas_text, text="")
            canvas.itemconfig(canvas_image, image=preview_img)

    def add_watermark(self):
        if self.file:
            self.image = Image.open(self.file)
            w = self.image.size[0]
            h = self.image.size[1]
            self.merged_image = Image.new("RGBA", (w, h))
            watermark_img_resized = copy.deepcopy(watermark_img).resize((w, h))
            self.merged_image.paste(self.image)
            self.merged_image.paste(watermark_img_resized, (0, 0), watermark_img_resized)
            # Creating a preview image
            watermark_preview = copy.deepcopy(self.merged_image)
            watermark_preview.thumbnail((500, 500))
            preview_img = ImageTk.PhotoImage(watermark_preview)
            # Next line is to prevent the image garbage collected when the function ends
            root.preview_img = preview_img
            canvas_image = canvas.create_image(250, 250, image=preview_img)
            canvas.itemconfig(canvas_text, text="")
            canvas.itemconfig(canvas_image, image=preview_img)

        else:
            messagebox.showerror(title="No Image Selected", message="Please select a file first")

    def save_file(self):
        if self.merged_image:
            save_file = filedialog.asksaveasfilename(filetypes=[('PNG', '*.png')], defaultextension='.png')
            if save_file:
                self.merged_image.save(save_file)
            else:
                messagebox.showerror(title="No Image Selected", message="Please select a file and watermark it first")
        else:
            messagebox.showerror(title="No Image Selected", message="Please select a file and watermark it first")


buttons = FileManager()

root.mainloop()
