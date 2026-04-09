# Cell 1 - Import required libraries
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


# Cell 2 - Function to clean filename
def clean_filename(filename):
    # Replace special characters with underscore
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)


# Cell 3 - Main processing function
def process_folder(folder_path, output_box):
    renamed_count = 0
    output_box.delete(1.0, tk.END)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            old_path = os.path.join(root, file)
            new_name = clean_filename(file)

            if file != new_name:
                new_path = os.path.join(root, new_name)

                try:
                    os.rename(old_path, new_path)
                    renamed_count += 1

                    output_box.insert(tk.END, f"Renamed:\n{file} → {new_name}\n\n")

                except Exception as e:
                    output_box.insert(tk.END, f"Error: {file} → {e}\n\n")

    output_box.insert(tk.END, f"\n✅ Total files renamed: {renamed_count}\n")


# Cell 4 - Browse folder function
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)


# Cell 5 - Start processing
def start_processing():
    folder_path = folder_path_var.get()

    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder!")
        return

    process_folder(folder_path, output_box)


# Cell 6 - Exit app
def exit_app():
    root.destroy()


# Cell 7 - GUI Setup
root = tk.Tk()
root.title("File Renamer Tool")
root.geometry("700x500")


# Folder path input
folder_path_var = tk.StringVar()

tk.Label(root, text="Select Folder:", font=("Arial", 12)).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Entry(frame, textvariable=folder_path_var, width=50).pack(side=tk.LEFT, padx=5)

tk.Button(frame, text="Browse", command=browse_folder).pack(side=tk.LEFT)


# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start", command=start_processing, bg="green", fg="white").pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame, text="Exit", command=exit_app, bg="red", fg="white").pack(side=tk.LEFT, padx=10)


# Output box
output_box = scrolledtext.ScrolledText(root, width=80, height=20)
output_box.pack(pady=10)


# Run GUI
root.mainloop()