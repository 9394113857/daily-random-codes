import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import os

class PDFViewerApp:
    def __init__(self, pdf_file):
        self.viewer_root = tk.Toplevel()
        self.viewer_root.title("PDF Viewer with Rotation and Pagination")
        self.pdf_path = pdf_file
        self.pdf_document = fitz.open(pdf_file)
        self.current_page = 0
        self.rotation_angles = [0] * len(self.pdf_document)  # Track rotation per page
        self.preview_canvas = None
        self.preview_image = None
        self.page_label = None
        self.init_gui()

    def init_gui(self):
        canvas_frame = ttk.Frame(self.viewer_root)
        canvas_frame.pack(expand=True, fill=tk.BOTH)

        self.preview_canvas = tk.Canvas(canvas_frame, width=800, height=600, bg="gray")
        self.preview_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.preview_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.preview_canvas.configure(yscrollcommand=scrollbar.set)
        self.preview_canvas.bind("<MouseWheel>", self.scroll_preview)
        self.viewer_root.bind("<Left>", lambda event: self.show_previous_page())
        self.viewer_root.bind("<Right>", lambda event: self.show_next_page())

        nav_frame = ttk.Frame(self.viewer_root)
        nav_frame.pack(pady=10)

        # Pagination Buttons
        ttk.Button(nav_frame, text="|< First", command=self.show_first_page).pack(side=tk.LEFT, padx=3)
        ttk.Button(nav_frame, text="< Prev", command=self.show_previous_page).pack(side=tk.LEFT, padx=3)
        ttk.Button(nav_frame, text="Next >", command=self.show_next_page).pack(side=tk.LEFT, padx=3)
        ttk.Button(nav_frame, text="Last >|", command=self.show_last_page).pack(side=tk.LEFT, padx=3)

        # Rotate Buttons
        ttk.Button(nav_frame, text="Rotate Left", command=self.rotate_left).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Rotate Right", command=self.rotate_right).pack(side=tk.LEFT, padx=10)

        # Save and Exit Buttons
        ttk.Button(nav_frame, text="Save PDF", command=self.save_pdf).pack(side=tk.LEFT, padx=15)
        ttk.Button(nav_frame, text="Exit", command=self.exit_app).pack(side=tk.LEFT, padx=15)

        # Page label showing current / total pages
        self.page_label = ttk.Label(nav_frame, text="Page: 0 of 0")
        self.page_label.pack(side=tk.LEFT, padx=20)

        self.show_page(self.current_page)

    def show_page(self, page_number):
        if page_number < 0 or page_number >= len(self.pdf_document):
            return
        page = self.pdf_document.load_page(page_number)
        rot = self.rotation_angles[page_number]
        mat = fitz.Matrix(2, 2).prerotate(rot)
        pix = page.get_pixmap(matrix=mat)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.preview_image = ImageTk.PhotoImage(image)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox(tk.ALL))
        total_pages = len(self.pdf_document)
        self.page_label.config(text=f"Page: {page_number + 1} of {total_pages}")
        self.current_page = page_number  # update current page

    def scroll_preview(self, event):
        if event.delta > 0:
            self.show_previous_page()
        elif event.delta < 0:
            self.show_next_page()

    def show_previous_page(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def show_next_page(self):
        if self.current_page < len(self.pdf_document) - 1:
            self.show_page(self.current_page + 1)

    def show_first_page(self):
        self.show_page(0)

    def show_last_page(self):
        self.show_page(len(self.pdf_document) - 1)

    def rotate_left(self):
        self.rotation_angles[self.current_page] = (self.rotation_angles[self.current_page] - 90) % 360
        self.show_page(self.current_page)

    def rotate_right(self):
        self.rotation_angles[self.current_page] = (self.rotation_angles[self.current_page] + 90) % 360
        self.show_page(self.current_page)

    def save_pdf(self):
        try:
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=[("PDF Files", "*.pdf")],
                                                     initialfile=os.path.basename(self.pdf_path))
            if not save_path:
                return
            new_pdf = fitz.open()
            for i in range(len(self.pdf_document)):
                page = self.pdf_document.load_page(i)
                rot = self.rotation_angles[i]
                # Copy page to new PDF
                new_pdf.insert_pdf(self.pdf_document, from_page=i, to_page=i)
                if rot != 0:
                    new_pdf[i].set_rotation(rot)
            new_pdf.save(save_path)
            new_pdf.close()
            messagebox.showinfo("Success", f"PDF saved successfully at:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{e}")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you want to save the PDF before exiting?"):
            self.save_pdf()
        self.viewer_root.destroy()

class PDFRotaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Rotater")
        self.pdf_file = None
        self.viewer_app = None
        self.init_gui()

    def init_gui(self):
        ttk.Button(self.root, text="Select PDF File", command=self.load_pdf).pack(pady=20)

    def load_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file:
            self.viewer_app = PDFViewerApp(self.pdf_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFRotaterApp(root)
    root.mainloop()
