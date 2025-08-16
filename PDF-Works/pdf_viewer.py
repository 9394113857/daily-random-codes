import os
from pdf2image import convert_from_path
from tkinter import Tk, Label, Button, Frame, LEFT
from PIL import Image, ImageTk

class PDFViewer:
    def __init__(self, master, pdf_files, pdf_folder):
        self.master = master
        self.pdf_files = pdf_files
        self.pdf_folder = pdf_folder
        self.current_pdf_index = 0
        self.pages = []
        self.current_page_index = 0

        master.title("PDF Viewer")

        self.label_file = Label(master, text="", font=("Arial", 14))
        self.label_file.pack(pady=5)

        self.image_label = Label(master)
        self.image_label.pack()

        nav_frame = Frame(master)
        nav_frame.pack(pady=5)

        self.btn_prev = Button(nav_frame, text="<< Prev Page", command=self.prev_page, width=15)
        self.btn_prev.pack(side=LEFT, padx=5)

        self.label_page = Label(nav_frame, text="Page 0/0", font=("Arial", 12))
        self.label_page.pack(side=LEFT, padx=5)

        self.btn_next = Button(nav_frame, text="Next Page >>", command=self.next_page, width=15)
        self.btn_next.pack(side=LEFT, padx=5)

        file_nav_frame = Frame(master)
        file_nav_frame.pack(pady=5)

        self.btn_prev_pdf = Button(file_nav_frame, text="<< Prev File", command=self.prev_pdf, width=15)
        self.btn_prev_pdf.pack(side=LEFT, padx=5)

        self.btn_next_pdf = Button(file_nav_frame, text="Next File >>", command=self.next_pdf, width=15)
        self.btn_next_pdf.pack(side=LEFT, padx=5)

        self.btn_exit = Button(master, text="EXIT", command=master.quit, bg="red", fg="white", font=("Arial", 16), width=20)
        self.btn_exit.pack(pady=10)

        self.load_pdf(self.current_pdf_index)

    def load_pdf(self, index):
        if index < 0 or index >= len(self.pdf_files):
            return
        pdf_path = os.path.join(self.pdf_folder, self.pdf_files[index])
        self.label_file.config(text=f"File: {self.pdf_files[index]}")

        print(f"Loading PDF: {pdf_path} ... This may take a few seconds.")
        self.pages = convert_from_path(pdf_path)
        self.current_page_index = 0
        self.show_page()

        self.btn_prev_pdf.config(state="normal" if index > 0 else "disabled")
        self.btn_next_pdf.config(state="normal" if index < len(self.pdf_files) -1 else "disabled")

    def show_page(self):
        if not self.pages:
            return
        page_img = self.pages[self.current_page_index]
        page_img = page_img.resize((600, 800))  # Resize to fit window nicely
        self.photo = ImageTk.PhotoImage(page_img)
        self.image_label.config(image=self.photo)
        self.label_page.config(text=f"Page {self.current_page_index + 1} / {len(self.pages)}")

        self.btn_prev.config(state="normal" if self.current_page_index > 0 else "disabled")
        self.btn_next.config(state="normal" if self.current_page_index < len(self.pages) - 1 else "disabled")

    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            self.show_page()

    def prev_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.show_page()

    def next_pdf(self):
        if self.current_pdf_index < len(self.pdf_files) - 1:
            self.current_pdf_index += 1
            self.load_pdf(self.current_pdf_index)

    def prev_pdf(self):
        if self.current_pdf_index > 0:
            self.current_pdf_index -= 1
            self.load_pdf(self.current_pdf_index)

def main():
    pdf_folder = input("Enter the full path to your PDF folder: ").strip()
    if not os.path.exists(pdf_folder) or not os.path.isdir(pdf_folder):
        print(f"Folder does not exist or is not a directory: {pdf_folder}")
        return

    pdf_files = sorted([f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")])
    if not pdf_files:
        print(f"No PDF files found in folder: {pdf_folder}")
        return

    root = Tk()
    root.geometry("650x950")
    app = PDFViewer(root, pdf_files, pdf_folder)
    root.mainloop()

if __name__ == "__main__":
    main()
