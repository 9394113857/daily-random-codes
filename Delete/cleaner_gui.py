import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

def bytes_to_mb(size):
    return round(size / (1024 * 1024), 4)

class FileCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder File Cleaner Utility")
        self.root.geometry("900x650")

        self.base_path = tk.StringVar()

        # ---------------------- UI SECTION ----------------------
        title = tk.Label(root, text="File Cleaner – Keep Folders, Delete Only Files",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Path selection
        path_frame = tk.Frame(root)
        path_frame.pack(pady=5)

        tk.Label(path_frame, text="Select Base Folder: ", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Entry(path_frame, textvariable=self.base_path, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(path_frame, text="Browse", command=self.select_path).pack(side=tk.LEFT)

        # Preview button
        tk.Button(root, text="Preview Files to Delete",
                  command=self.preview_files, width=30).pack(pady=10)

        # Table Area
        self.tree = ttk.Treeview(root, columns=("sno", "file", "size", "folder"), show="headings")
        self.tree.heading("sno", text="Sno")
        self.tree.heading("file", text="File Name")
        self.tree.heading("size", text="Size (MB)")
        self.tree.heading("folder", text="Folder")

        self.tree.column("sno", width=50, anchor='center')
        self.tree.column("file", width=250)
        self.tree.column("size", width=100, anchor='center')
        self.tree.column("folder", width=400)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Action Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Delete Files", command=self.delete_files,
                  width=20, bg="red", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Exit", command=root.quit,
                  width=20, bg="black", fg="white").pack(side=tk.LEFT, padx=10)

        self.files_list = []  # store preview files

    # ------------------------------------------------------------------
    def select_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.base_path.set(folder)

    # ------------------------------------------------------------------
    def preview_files(self):
        base = self.base_path.get().strip()
        if not base:
            messagebox.showwarning("Warning", "Please select a folder path.")
            return

        self.tree.delete(*self.tree.get_children())
        self.files_list.clear()

        sno = 1
        total_size = 0

        for root_dir, dirs, files in os.walk(base):
            for f in files:
                full_path = os.path.join(root_dir, f)
                size = os.path.getsize(full_path)
                total_size += size

                self.files_list.append((full_path, size))

                self.tree.insert("", "end",
                                 values=(sno, f, bytes_to_mb(size), root_dir))
                sno += 1
        
        if sno == 1:
            messagebox.showinfo("Info", "No files found. Only folders exist.")
        else:
            messagebox.showinfo("Preview Ready",
                                f"Total files found: {sno-1}\nTotal size: {bytes_to_mb(total_size)} MB")

    # ------------------------------------------------------------------
    def delete_files(self):
        if not self.files_list:
            messagebox.showwarning("Warning", "Preview not done or no files found.")
            return

        confirm = messagebox.askyesno("Confirm Delete",
                                      "Are you sure you want to delete ALL these files?\nFolders will be kept safely.")
        if not confirm:
            return

        deleted_space = 0
        deleted_count = 0

        for fpath, size in self.files_list:
            try:
                os.remove(fpath)
                deleted_space += size
                deleted_count += 1
            except:
                pass

        messagebox.showinfo("Delete Completed",
                            f"Deleted Files: {deleted_count}\n"
                            f"Space Freed: {bytes_to_mb(deleted_space)} MB")

        # Clear preview table
        self.tree.delete(*self.tree.get_children())
        self.files_list.clear()


# ----------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FileCleanerGUI(root)
    root.mainloop()
