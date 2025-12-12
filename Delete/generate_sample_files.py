import os
import random
import string
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


def random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".txt"


def random_content(size_kb=5):
    return ''.join(random.choices(string.ascii_letters + string.digits + " ", k=size_kb * 1024))


class SampleDataGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Sample Folder & File Generator")
        self.root.geometry("450x220")

        self.base_path = tk.StringVar()

        tk.Label(root, text="Select Base Path to Generate Sample Data",
                 font=("Arial", 12, "bold")).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Entry(frame, textvariable=self.base_path, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Browse", command=self.select_path).pack(side=tk.LEFT)

        tk.Button(root, text="Generate Sample Structure",
                  width=30, command=self.generate_sample).pack(pady=15)

        tk.Button(root, text="Exit", width=20, command=root.quit,
                  bg="black", fg="white").pack(pady=10)

    # --------------------------------------------------------------
    def select_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.base_path.set(folder)

    # --------------------------------------------------------------
    def generate_sample(self):
        base = self.base_path.get().strip()

        if not base:
            messagebox.showwarning("Warning", "Please choose a base path.")
            return

        base = Path(base)

        # Subfolders to create
        subfolders = ["Folder_A", "Folder_B", "Folder_C",
                      "Folder_A/Sub_1", "Folder_B/Sub_2"]

        created_files = 0

        for sub in subfolders:
            folder_path = base / sub
            folder_path.mkdir(parents=True, exist_ok=True)

            # Create 2–4 random files per folder
            for _ in range(random.randint(2, 4)):
                filename = random_filename()
                file_path = folder_path / filename

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(random_content(size_kb=random.randint(3, 10)))

                created_files += 1

        messagebox.showinfo("Success",
                            f"Sample folders and files created!\n\nTotal Files: {created_files}")


# --------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SampleDataGenerator(root)
    root.mainloop()
