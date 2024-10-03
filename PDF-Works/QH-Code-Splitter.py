import os
import PyPDF2
from tkinter import Tk, filedialog, Button, Label, Entry, StringVar, END, messagebox

class PDFSplitter:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Splitter")
        self.master.geometry("400x300")

        self.pdf_file = None
        self.pdf_reader = None
        self.output_path = None

        # PDF File Selection Label
        self.file_label = Label(master, text="No file selected")
        self.file_label.pack(pady=5)

        self.select_button = Button(master, text="Select PDF File", command=self.select_pdf_file)
        self.select_button.pack(pady=5)

        # Start Page
        self.start_label = Label(master, text="Start Page:")
        self.start_label.pack(pady=5)

        self.start_page_var = StringVar()
        self.start_entry = Entry(master, textvariable=self.start_page_var)
        self.start_entry.pack(pady=5)

        # End Page
        self.end_label = Label(master, text="End Page:")
        self.end_label.pack(pady=5)

        self.end_page_var = StringVar()
        self.end_entry = Entry(master, textvariable=self.end_page_var)
        self.end_entry.pack(pady=5)

        # Output File Name
        self.output_label = Label(master, text="Output File Name:")
        self.output_label.pack(pady=5)

        self.output_file_var = StringVar()
        self.output_entry = Entry(master, textvariable=self.output_file_var)
        self.output_entry.pack(pady=5)

        # Save Button
        self.save_button = Button(master, text="Save Selected Pages", command=self.save_selected_pages)
        self.save_button.pack(pady=5)

        # Output Directory Button
        self.output_button = Button(master, text="Select Output Directory", command=self.select_output_directory)
        self.output_button.pack(pady=5)

        # Exit Button
        self.exit_button = Button(master, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=5)

    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_file = open(file_path, "rb")
            self.pdf_reader = PyPDF2.PdfReader(self.pdf_file)
            self.file_label.config(text=f"Selected File: {file_path}")

    def select_output_directory(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            messagebox.showinfo("Output Directory Selected", f"Selected Output Directory: {self.output_path}")

    def save_selected_pages(self):
        try:
            start_page = int(self.start_page_var.get())
            end_page = int(self.end_page_var.get())
            input_file_name = self.output_file_var.get()

            if not input_file_name:
                messagebox.showerror("Error", "Please provide an output file name.")
                return

            if not self.output_path:
                messagebox.showerror("Error", "Please select an output directory.")
                return

            output_file_name = f"QH-{input_file_name}_2024-25.pdf"
            output_path = os.path.join(self.output_path, output_file_name)

            self.pdf_writer = PyPDF2.PdfWriter()

            for page_num in range(start_page - 1, end_page):
                self.pdf_writer.add_page(self.pdf_reader.pages[page_num])

            with open(output_path, "wb") as output_file:
                self.pdf_writer.write(output_file)

            messagebox.showinfo("Success", f"Pages {start_page} to {end_page} saved successfully to {output_path}.")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_entries(self):
        self.start_entry.delete(0, END)
        self.end_entry.delete(0, END)
        self.output_entry.delete(0, END)

    def exit_app(self):
        if self.pdf_file:
            self.pdf_file.close()
        self.master.quit()

def main():
    root = Tk()
    app = PDFSplitter(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Both QH and QM paths are taken if not and remaining both files flow same accordingly only.