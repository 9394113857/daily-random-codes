import os
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import csv

# Function to display PDFs on the current page
def display_pdfs(page_number, pdf_files, files_per_page=5):
    start_index = (page_number - 1) * files_per_page
    end_index = start_index + files_per_page
    files_to_display = pdf_files[start_index:end_index]

    # Clear the treeview before displaying new data
    for row in treeview.get_children():
        treeview.delete(row)

    # Insert the files in the table with pagination
    for i, file_name in enumerate(files_to_display, start=start_index + 1):
        treeview.insert("", "end", values=(i, file_name))

    # Update the page info
    page_label.config(text=f"Page {page_number} of {total_pages}")

    # Disable buttons when appropriate
    first_button.config(state="normal" if page_number > 1 else "disabled")
    prev_button.config(state="normal" if page_number > 1 else "disabled")
    next_button.config(state="normal" if page_number < total_pages else "disabled")
    last_button.config(state="normal" if page_number < total_pages else "disabled")

# Function to go to the first page
def first_page():
    global current_page
    current_page = 1
    display_pdfs(current_page, pdf_files)

# Function to go to the last page
def last_page():
    global current_page
    current_page = total_pages
    display_pdfs(current_page, pdf_files)

# Function to handle next page
def next_page():
    global current_page
    current_page += 1
    display_pdfs(current_page, pdf_files)

# Function to handle previous page
def prev_page():
    global current_page
    current_page -= 1
    display_pdfs(current_page, pdf_files)

# Function to save the PDF filenames to a CSV file
def save_output():
    # Prompt the user to choose a directory to save the CSV file
    save_directory = filedialog.askdirectory(title="Select Directory to Save CSV")
    
    if save_directory:  # Ensure the user has not cancelled the dialog
        # Prompt for the filename
        csv_filename = tk.simpledialog.askstring("Input", "Enter the name of the CSV file (without .csv extension):")
        
        if csv_filename:
            # Create the full path for the CSV file
            full_path = os.path.join(save_directory, f"{csv_filename}.csv")
            
            # Write the PDF filenames to the CSV file
            with open(full_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write the header
                csv_writer.writerow(["S.No", "Invoice"])
                # Write the data
                for index, pdf in enumerate(pdf_files, start=1):
                    csv_writer.writerow([index, pdf])
            
            messagebox.showinfo("Success", f"Saved output to {full_path}")
        else:
            messagebox.showerror("Error", "Please provide a valid CSV filename.")
    else:
        messagebox.showwarning("Warning", "Save operation was cancelled.")

# Function to close the application
def exit_app():
    root.destroy()

# Function to initialize the main window
def main_window(directory, window_title):
    global pdf_files, total_pages, current_page, root, treeview, page_label, first_button, prev_button, next_button, last_button

    # Create the main window
    root = tk.Tk()
    root.title("PDF Viewer with Pagination")

    # Display the title inside the window, bold and centered
    title_font = font.Font(root, size=14, weight="bold")
    title_label = tk.Label(root, text=window_title if window_title else "PDF Viewer", font=title_font)
    title_label.pack(pady=10)

    # Table (Treeview)
    treeview = ttk.Treeview(root, columns=("S.No", "Invoice"), show="headings", height=8)
    treeview.heading("S.No", text="S.No")
    treeview.heading("Invoice", text="Invoice")
    treeview.pack(pady=10)

    # Pagination controls
    pagination_frame = tk.Frame(root)
    pagination_frame.pack()

    first_button = tk.Button(pagination_frame, text="First", command=first_page, state="disabled")
    first_button.grid(row=0, column=0)

    prev_button = tk.Button(pagination_frame, text="Previous", command=prev_page, state="disabled")
    prev_button.grid(row=0, column=1)

    page_label = tk.Label(pagination_frame, text="Page 1")
    page_label.grid(row=0, column=2, padx=20)

    next_button = tk.Button(pagination_frame, text="Next", command=next_page, state="disabled")
    next_button.grid(row=0, column=3)

    last_button = tk.Button(pagination_frame, text="Last", command=last_page, state="disabled")
    last_button.grid(row=0, column=4)

    # Exit Button
    exit_button = tk.Button(root, text="Exit", command=exit_app)
    exit_button.pack(pady=10)

    # Save Button
    save_button = tk.Button(root, text="Save Output", command=save_output)
    save_button.pack(pady=10)

    # Load PDF files from the directory
    files = os.listdir(directory)
    pdf_files = [f for f in files if f.endswith('.pdf')]

    if not pdf_files:
        messagebox.showinfo("Info", "No PDF files found in the directory.")
        root.destroy()
        return

    # Pagination setup
    current_page = 1
    files_per_page = 5
    total_pages = (len(pdf_files) + files_per_page - 1) // files_per_page

    # Display the first page
    display_pdfs(current_page, pdf_files)

    # Start the Tkinter event loop
    root.mainloop()

# Function to handle the initial input window
def input_window():
    def on_ok():
        directory = dir_entry.get()
        window_title = title_entry.get()
        
        # Validate directory path
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Invalid directory path.")
            return

        if not window_title.strip():  # Ensure title is not empty
            messagebox.showerror("Error", "Window title cannot be empty.")
            return
        
        # Close input window and open the main window
        input_win.destroy()
        main_window(directory, window_title)

    # Create the input window
    input_win = tk.Tk()
    input_win.title("Input Required")

    # Directory Path Input
    tk.Label(input_win, text="Enter Directory Path:").grid(row=0, column=0, padx=10, pady=5)
    dir_entry = tk.Entry(input_win, width=40)
    dir_entry.grid(row=0, column=1, padx=10, pady=5)

    # Button to select directory
    select_button = tk.Button(input_win, text="Select", command=lambda: dir_entry.insert(0, filedialog.askdirectory()))
    select_button.grid(row=0, column=2, padx=5)

    # Window Title Input
    tk.Label(input_win, text="Enter Window Title:").grid(row=1, column=0, padx=10, pady=5)
    title_entry = tk.Entry(input_win, width=40)
    title_entry.grid(row=1, column=1, padx=10, pady=5)

    # OK Button
    ok_button = tk.Button(input_win, text="OK", command=on_ok)
    ok_button.grid(row=2, columnspan=3, pady=10)

    # Start the input window loop
    input_win.mainloop()

# Start the input window first
input_window()
