import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Invoice Viewer")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = ttk.Label(self.root, text="PDF Invoice Viewer", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        select_btn = ttk.Button(button_frame, text="Select Directory", command=self.select_directory)
        select_btn.grid(row=0, column=0, padx=10)

        exit_btn = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_btn.grid(row=0, column=1, padx=10)

        # Treeview (Table)
        columns = ("S.No", "Invoice", "Size")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)

        # Define headings
        self.tree.heading("S.No", text="S.No")
        self.tree.heading("Invoice", text="Invoice")
        self.tree.heading("Size", text="Size")

        # Set fixed column widths and alignment
        self.tree.column("S.No", width=70, anchor="center")
        self.tree.column("Invoice", width=540, anchor="w")
        self.tree.column("Size", width=120, anchor="e")

        self.tree.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Optional: Set monospaced font to improve column alignment
        style = ttk.Style()
        style.configure("Treeview", font=("Courier New", 10))  # Use monospaced font

    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Directory")

        if not directory:
            return  # User cancelled

        if not os.path.exists(directory):
            messagebox.showerror("Error", "Invalid directory path.")
            return

        files = os.listdir(directory)
        pdf_files = [f for f in files if f.lower().endswith(".pdf")]

        # Clear previous entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not pdf_files:
            messagebox.showinfo("No PDFs", "No PDF files found in the selected directory.")
            return

        for idx, pdf in enumerate(sorted(pdf_files), start=1):
            full_path = os.path.join(directory, pdf)
            size_bytes = os.path.getsize(full_path)
            size_str = self.format_size(size_bytes)

            self.tree.insert("", "end", values=(str(idx), pdf, size_str))

    def format_size(self, size_bytes):
        """Formats bytes to KB or MB string, aligned properly."""
        if size_bytes >= 1024 * 1024:
            size_mb = size_bytes / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        else:
            size_kb = size_bytes / 1024
            return f"{size_kb:.2f} KB"

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewerApp(root)
    root.mainloop()
