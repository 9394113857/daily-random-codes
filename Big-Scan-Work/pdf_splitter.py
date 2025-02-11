import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import fitz  # PyMuPDF for PDF rendering
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
        # Frame for canvas and scrollbar
        canvas_frame = ttk.Frame(self.viewer_root)
        canvas_frame.pack(expand=True, fill=tk.BOTH)

        # Canvas for PDF preview
        self.preview_canvas = tk.Canvas(canvas_frame, width=800, height=600, bg="gray")
        self.preview_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Scrollbar for the canvas
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.preview_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas to work with scrollbar
        self.preview_canvas.configure(yscrollcommand=scrollbar.set)

        # Add mouse wheel scroll functionality
        self.preview_canvas.bind("<MouseWheel>", self.scroll_preview)

        # Bind keyboard left and right arrows for navigation
        self.viewer_root.bind("<Left>", lambda event: self.show_previous_page())
        self.viewer_root.bind("<Right>", lambda event: self.show_next_page())

        # Navigation buttons and page label
        nav_frame = ttk.Frame(self.viewer_root)
        nav_frame.pack(pady=10)

        prev_button = ttk.Button(nav_frame, text="Previous Page", command=self.show_previous_page)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = ttk.Button(nav_frame, text="Next Page", command=self.show_next_page)
        next_button.pack(side=tk.LEFT, padx=5)

        # Label to display the current page number
        self.page_label = ttk.Label(nav_frame, text="Page: 0 of 0")
        self.page_label.pack(side=tk.LEFT, padx=10)

        # Display the first page
        self.show_page(self.current_page)

    def show_page(self, page_number):
        if page_number < 0 or page_number >= len(self.pdf_document):
            return

        # Get the page and render it
        page = self.pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Scale for better quality
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Convert to ImageTk for Tkinter
        self.preview_image = ImageTk.PhotoImage(image)
        self.preview_canvas.delete("all")  # Clear previous content
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)

        # Adjust canvas size to fit content
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox(tk.ALL))

        # Update page label
        total_pages = len(self.pdf_document)
        self.page_label.config(text=f"Page: {page_number + 1} of {total_pages}")

    def scroll_preview(self, event):
        """Handle mouse wheel scrolling."""
        if event.delta > 0:  # Scroll up
            self.show_previous_page()
        elif event.delta < 0:  # Scroll down
            self.show_next_page()

    def show_previous_page(self):
        """Navigate to the previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def show_next_page(self):
        """Navigate to the next page."""
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
        # Select PDF file button
        self.select_file_button = ttk.Button(self.root, text="Select PDF File", command=self.load_pdf)
        self.select_file_button.pack(pady=10)

        # Frame for splitting options
        split_frame = ttk.Frame(self.root)
        split_frame.pack(pady=10)

        # Input for page ranges
        ttk.Label(split_frame, text="Page Ranges (e.g., 1-3, 5, 10-2):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.page_ranges_entry = ttk.Entry(split_frame, width=20)
        self.page_ranges_entry.grid(row=0, column=1, padx=5, pady=5)

        # Input for file prefix
        ttk.Label(split_frame, text="File Name Prefix:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.file_prefix_entry = ttk.Entry(split_frame, width=20)
        self.file_prefix_entry.grid(row=1, column=1, padx=5, pady=5)

        # Split and Save buttons
        self.split_button = ttk.Button(self.root, text="Split PDF", command=self.split_pdf)
        self.split_button.pack(pady=10)

    def load_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file:
            self.viewer_app = PDFViewerApp(self.pdf_file)

    def split_pdf(self):
        if not self.pdf_file:
            messagebox.showerror("Error", "No PDF file selected!")
            return

        page_ranges = self.page_ranges_entry.get()
        file_prefix = self.file_prefix_entry.get()
        if not page_ranges or not file_prefix:
            messagebox.showerror("Error", "Page ranges and file prefix are required!")
            return

        try:
            output_dir = filedialog.askdirectory(title="Select Output Directory")
            if not output_dir:
                messagebox.showerror("Error", "No output directory selected!")
                return

            pdf = fitz.open(self.pdf_file)
            ranges = self.parse_page_ranges(page_ranges, len(pdf))
            for idx, page_range in enumerate(ranges):
                output_pdf = fitz.open()
                for page_num in page_range:
                    output_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)

                # Save the output file
                output_filename = f"{file_prefix}_{idx + 1}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                output_pdf.save(output_path)
                output_pdf.close()

                # Show separate alerts for path and file name
                self.show_success_message(os.path.basename(output_dir), output_filename)

            pdf.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to split PDF: {e}")

    def parse_page_ranges(self, page_ranges, total_pages):
        """
        Parse and handle dynamic page ranges, including ascending and descending ranges.
        """
        ranges = []
        for part in page_ranges.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                # Ensure ranges work regardless of order (ascending or descending)
                step = 1 if start <= end else -1
                ranges.append(range(start - 1, end - 1 + step, step))
            else:
                ranges.append([int(part) - 1])
        return ranges

    def show_success_message(self, last_dir, file_name):
        # Show last directory in big text
        dir_popup = tk.Toplevel()
        dir_popup.title("Saved Directory")
        dir_popup.geometry("500x300")
        tk.Label(dir_popup, text=f"Directory:\n\n{last_dir}", font=("Arial", 24, "bold")).pack(expand=True, padx=20, pady=20)
        tk.Button(dir_popup, text="OK", command=dir_popup.destroy, font=("Arial", 16)).pack(pady=20)

        # Show file name in big text
        file_popup = tk.Toplevel()
        file_popup.title("Saved File Name")
        file_popup.geometry("500x300")
        tk.Label(file_popup, text=f"File Name:\n\n{file_name}", font=("Arial", 24, "bold")).pack(expand=True, padx=20, pady=20)
        tk.Button(file_popup, text="OK", command=file_popup.destroy, font=("Arial", 16)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
