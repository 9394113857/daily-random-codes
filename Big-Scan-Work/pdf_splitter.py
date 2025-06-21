import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import os

class PDFViewerApp:
    def __init__(self, pdf_file):
        self.viewer_root = tk.Toplevel()
        self.viewer_root.title("PDF Viewer")
        self.pdf_document = fitz.open(pdf_file)
        self.current_page = 0
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

        ttk.Button(nav_frame, text="Previous Page", command=self.show_previous_page).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Next Page", command=self.show_next_page).pack(side=tk.LEFT, padx=5)

        self.page_label = ttk.Label(nav_frame, text="Page: 0 of 0")
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.show_page(self.current_page)

    def show_page(self, page_number):
        if page_number < 0 or page_number >= len(self.pdf_document):
            return
        page = self.pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.preview_image = ImageTk.PhotoImage(image)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox(tk.ALL))
        total_pages = len(self.pdf_document)
        self.page_label.config(text=f"Page: {page_number + 1} of {total_pages}")

    def scroll_preview(self, event):
        if event.delta > 0:
            self.show_previous_page()
        elif event.delta < 0:
            self.show_next_page()

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def show_next_page(self):
        if self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.show_page(self.current_page)

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")
        self.pdf_file = None
        self.viewer_app = None
        self.init_gui()

    def init_gui(self):
        ttk.Button(self.root, text="Select PDF File", command=self.load_pdf).pack(pady=10)

        split_frame = ttk.Frame(self.root)
        split_frame.pack(pady=10)

        # File Name Prefix input first
        ttk.Label(split_frame, text="File Name Prefix:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.file_prefix_entry = ttk.Entry(split_frame, width=25)
        self.file_prefix_entry.grid(row=0, column=1, padx=5, pady=5)

        # Page Ranges input second
        ttk.Label(split_frame, text="Page Ranges (e.g., 1-52, 55, 60-57):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.page_ranges_entry = ttk.Entry(split_frame, width=25)
        self.page_ranges_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Split PDF", command=self.split_pdf).pack(pady=10)

    def load_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file:
            self.viewer_app = PDFViewerApp(self.pdf_file)

    def split_pdf(self):
        if not self.pdf_file:
            messagebox.showerror("Error", "No PDF file selected!")
            return

        file_prefix = self.file_prefix_entry.get().strip()
        page_ranges = self.page_ranges_entry.get().strip()

        if not page_ranges or not file_prefix:
            messagebox.showerror("Error", "File prefix and page ranges are required!")
            return

        try:
            output_dir = filedialog.askdirectory(title="Select Output Directory")
            if not output_dir:
                messagebox.showerror("Error", "No output directory selected!")
                return

            pdf = fitz.open(self.pdf_file)
            ranges = self.parse_page_ranges(page_ranges, len(pdf))

            output_pdf = fitz.open()
            for page_range in ranges:
                for page_num in page_range:
                    output_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)

            output_filename = f"{file_prefix}.pdf"
            output_path = os.path.join(output_dir, output_filename)

            if os.path.exists(output_path):
                os.remove(output_path)

            output_pdf.save(output_path)
            output_pdf.close()
            pdf.close()

            self.show_success_message(output_filename)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to split PDF: {e}")

    def parse_page_ranges(self, page_ranges, total_pages):
        ranges = []
        for part in page_ranges.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    if start < 1 or end < 1 or start > total_pages or end > total_pages:
                        raise ValueError("Page number out of range")
                    step = 1 if start <= end else -1
                    ranges.append(range(start - 1, end - 1 + step, step))
                else:
                    page_num = int(part.strip())
                    if page_num < 1 or page_num > total_pages:
                        raise ValueError("Page number out of range")
                    ranges.append([page_num - 1])
            except Exception:
                raise ValueError(f"Invalid page range: '{part}'")
        return ranges

    def show_success_message(self, file_name):
        file_popup = tk.Toplevel()
        file_popup.title("Saved File Name")
        file_popup.geometry("500x300")
        tk.Label(file_popup, text=f"File Name:\n\n{file_name}", font=("Arial", 24, "bold")).pack(expand=True, padx=20, pady=20)
        tk.Button(file_popup, text="OK", command=file_popup.destroy, font=("Arial", 16)).pack(pady=20)

if __name__ == "__main__": 
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
