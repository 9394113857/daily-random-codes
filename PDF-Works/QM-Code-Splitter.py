import os
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import PyPDF2
from tkinter import (
    Tk, Toplevel, filedialog, Button, Label, Entry, StringVar,
    messagebox, Canvas, Frame, BOTH, YES
)


class PDFSplitter:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Splitter")
        self.master.geometry("600x400")
        self.master.configure(bg="white")

        self.pdf_file_path = None
        self.pdf_reader = None
        self.doc = None
        self.current_page_index = 0
        self.rotations = {}
        self.deleted_pages = set()
        self.output_path = None

        self.select_button = Button(master, text="Select PDF File", command=self.select_pdf_file,
                                    width=25, font=("Arial", 12))
        self.select_button.pack(pady=40)

        self.output_file_var = StringVar()
        self.page_range_var = StringVar()

        self.output_label = None
        self.output_entry = None
        self.range_label = None
        self.range_entry = None
        self.save_button = None

    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_file_path = file_path
            self.pdf_reader = PyPDF2.PdfReader(open(file_path, "rb"))
            self.doc = fitz.open(file_path)
            self.rotations = {i: 0 for i in range(len(self.doc))}
            self.deleted_pages = set()
            self.current_page_index = 0

            self.master.title(f"PDF Splitter - {os.path.basename(file_path)}")

            self.show_preview_window()
            self.show_input_widgets()

    def show_input_widgets(self):
        if self.output_label is None:
            self.output_label = Label(self.master, text="Output File Name (e.g. QM-0001):", bg="white")
            self.output_label.pack(pady=(10, 2))
        if self.output_entry is None:
            self.output_entry = Entry(self.master, textvariable=self.output_file_var, width=30)
            self.output_entry.pack()

        if self.range_label is None:
            self.range_label = Label(self.master, text="Page Range (e.g. 2-5):", bg="white")
            self.range_label.pack(pady=(10, 2))
        if self.range_entry is None:
            self.range_entry = Entry(self.master, textvariable=self.page_range_var, width=30)
            self.range_entry.pack()

        if self.save_button is None:
            self.save_button = Button(self.master, text="Export Pages", command=self.save_selected_pages,
                                      width=20, font=("Arial", 12))
            self.save_button.pack(pady=15)

    def show_preview_window(self):
        self.preview_win = Toplevel(self.master)
        self.preview_win.title(f"Preview - {os.path.basename(self.pdf_file_path)}")
        # Start with a decent size, but allow resizing fully
        self.preview_win.geometry("820x900")
        self.preview_win.minsize(600, 700)  # minimum window size so it doesn't shrink too much
        self.preview_win.configure(bg="white")

        # Use grid for main_frame to allow better resizing control
        main_frame = Frame(self.preview_win, bg="white")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.preview_win.grid_rowconfigure(0, weight=1)
        self.preview_win.grid_columnconfigure(0, weight=1)

        # Canvas with expandable size
        self.canvas = Canvas(main_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Page label below canvas
        self.page_label = Label(main_frame, text="", font=("Arial", 14), bg="white")
        self.page_label.grid(row=1, column=0, pady=5)

        # Button frame below label
        btn_frame = Frame(main_frame, bg="white")
        btn_frame.grid(row=2, column=0, pady=10, sticky="ew")

        # Configure main_frame rows and columns for resizing
        main_frame.grid_rowconfigure(0, weight=1)  # canvas expands vertically
        main_frame.grid_columnconfigure(0, weight=1)  # canvas expands horizontally

        # Buttons in btn_frame - grid layout with spacing and sticky so they stay visible
        btn_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)  # distribute buttons equally

        Button(btn_frame, text="Previous", width=12, command=self.show_previous_page).grid(row=0, column=0, padx=5, sticky="ew")
        Button(btn_frame, text="Next", width=12, command=self.show_next_page).grid(row=0, column=1, padx=5, sticky="ew")
        Button(btn_frame, text="Rotate Left", width=12, command=self.rotate_left).grid(row=0, column=2, padx=5, sticky="ew")
        Button(btn_frame, text="Rotate Right", width=12, command=self.rotate_right).grid(row=0, column=3, padx=5, sticky="ew")
        Button(btn_frame, text="Delete Page", width=12, fg="white", bg="red", command=self.delete_current_page).grid(row=0, column=4, padx=5, sticky="ew")

        # Bind resize event to update image scaling
        self.preview_win.bind("<Configure>", self.on_resize)

        self.update_preview_image()

    def on_resize(self, event):
        # Called when preview window or widgets resize
        # Update preview image to fit new canvas size
        # Use after_idle to avoid multiple calls in rapid succession
        self.preview_win.after_idle(self.update_preview_image)

    def update_preview_image(self):
        if not self.doc or len(self.doc) == 0:
            self.canvas.delete("all")
            self.page_label.config(text="No pages to display.")
            return

        # Skip deleted pages if current is deleted
        while self.current_page_index in self.deleted_pages:
            self.current_page_index += 1
            if self.current_page_index >= len(self.doc):
                self.current_page_index = 0

        page = self.doc.load_page(self.current_page_index)
        rot = self.rotations.get(self.current_page_index, 0)

        # Get current canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Sometimes at startup canvas size is 1, ignore
            return

        # Render pixmap at 2x scale before rotation for quality
        mat = fitz.Matrix(2, 2).prerotate(rot)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Calculate scaling to fit inside canvas
        scale = min(canvas_width / img.width, canvas_height / img.height, 1)
        new_w = int(img.width * scale)
        new_h = int(img.height * scale)

        img_resized = img.resize((new_w, new_h), Image.LANCZOS)

        self.tk_img = ImageTk.PhotoImage(img_resized)
        self.canvas.delete("all")
        # Center image in canvas horizontally and vertically
        x = (canvas_width - new_w) // 2
        y = (canvas_height - new_h) // 2
        self.canvas.create_image(x, y, anchor="nw", image=self.tk_img)

        self.page_label.config(
            text=f"Page {self.current_page_index + 1} of {len(self.doc)} | Rotation: {rot}° (Deleted: {len(self.deleted_pages)})"
        )

    def show_next_page(self):
        next_index = self.current_page_index + 1
        while next_index < len(self.doc) and next_index in self.deleted_pages:
            next_index += 1
        if next_index < len(self.doc):
            self.current_page_index = next_index
            self.update_preview_image()

    def show_previous_page(self):
        prev_index = self.current_page_index - 1
        while prev_index >= 0 and prev_index in self.deleted_pages:
            prev_index -= 1
        if prev_index >= 0:
            self.current_page_index = prev_index
            self.update_preview_image()

    def rotate_left(self):
        if self.current_page_index in self.deleted_pages:
            return
        self.rotations[self.current_page_index] = (self.rotations.get(self.current_page_index, 0) - 90) % 360
        self.update_preview_image()

    def rotate_right(self):
        if self.current_page_index in self.deleted_pages:
            return
        self.rotations[self.current_page_index] = (self.rotations.get(self.current_page_index, 0) + 90) % 360
        self.update_preview_image()

    def delete_current_page(self):
        if self.current_page_index in self.deleted_pages:
            messagebox.showinfo("Info", "Page already deleted.")
            return

        confirm = messagebox.askyesno("Delete Page", f"Delete page {self.current_page_index + 1}?")
        if not confirm:
            return

        self.deleted_pages.add(self.current_page_index)
        self.show_next_page()

        if len(self.deleted_pages) == len(self.doc):
            messagebox.showinfo("Info", "All pages deleted.")
            self.canvas.delete("all")
            self.page_label.config(text="No pages to display.")

    def save_selected_pages(self):
        # Placeholder - implement your export logic here
        pass


if __name__ == "__main__":
    root = Tk()
    app = PDFSplitter(root)
    root.mainloop()
