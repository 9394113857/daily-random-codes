import os  # Importing the os module for interacting with the file system
import tkinter as tk  # Importing tkinter for creating GUI applications
from tkinter import ttk, messagebox, filedialog  # Importing additional tkinter components: Treeview, message boxes, and file dialogs
import math  # Importing the math module to handle pagination calculations

# Function to open a folder selection dialog and display its contents
def select_folder(window):
    folder_path = filedialog.askdirectory()  # Open a dialog for the user to select a folder
    if folder_path:  # If a valid folder is selected
        display_file_tree(window, folder_path)  # Call the function to display the folder's contents in a tree structure

# Function to display the folder contents in a table-like format with pagination
def display_file_tree(window, folder_path):
    # Clear any existing content in the window
    for widget in window.winfo_children():
        widget.destroy()

    # Create a Treeview widget to display the files and folders in columns
    tree = ttk.Treeview(window, columns=("S.No", "File/Folder"), show="headings")  # Create tree columns: S.No and File/Folder
    tree.heading("S.No", text="S.No")  # Set the heading for Serial Number column
    tree.heading("File/Folder", text="File/Folder")  # Set the heading for File/Folder column
    tree.pack(fill=tk.BOTH, expand=True)  # Make the tree fill the available space in the window

    all_items = []  # Initialize a list to hold all file and folder names in the selected folder

    # Function to recursively insert files and folders into the tree
    def insert_files(parent, folder):
        try:
            # Get a sorted list of items (files and folders) in the directory
            items = sorted(os.listdir(folder))
            for item in items:
                path = os.path.join(folder, item)  # Get the full path for the item
                all_items.append(item)  # Add the item to the list of all items
                if os.path.isdir(path):  # If the item is a folder
                    insert_files(parent, path)  # Recursively insert its contents
        except PermissionError:  # Handle permission errors when trying to access restricted folders
            pass  # Skip the folder if permission is denied

    insert_files("", folder_path)  # Call the function to insert files starting from the selected folder

    # If no items are found in the folder, show a message and return
    if not all_items:
        messagebox.showinfo("No Files Found", f"No files or folders found in {folder_path}")
        return  # Exit the function if the folder is empty

    # Pagination settings: how many items to display per page
    items_per_page = 10  # Set the number of items to display on each page
    current_page = [1]  # Keep track of the current page in a mutable list
    total_pages = math.ceil(len(all_items) / items_per_page)  # Calculate the total number of pages

    # Create a label to display the current page number and total pages
    page_label = tk.Label(window, text=f"Page {current_page[0]} of {total_pages}", font=("Arial", 12))  # Page label
    page_label.pack(pady=5)  # Add some padding around the page label

    # Function to update the Treeview with items for the current page
    def update_tree(filtered_items):
        tree.delete(*tree.get_children())  # Clear the current items in the Treeview

        # Determine the start and end index for the items on the current page
        start = (current_page[0] - 1) * items_per_page  # Start index
        end = min(start + items_per_page, len(filtered_items))  # End index (ensure we don't exceed the item count)

        # Insert the items for the current page into the Treeview with serial numbers
        for idx in range(start, end):
            item = filtered_items[idx]  # Get the item
            tree.insert("", "end", values=(idx + 1, item))  # Insert the item into the Treeview

        # Update the page label to reflect the current page
        page_label.config(text=f"Page {current_page[0]} of {total_pages}")  # Update page number in the label

    # Function to apply file extension filters based on user input
    def apply_filter():
        filter_text = filter_entry.get()  # Get the filter input from the entry field
        filters = [ext.strip() for ext in filter_text.split(",") if ext.strip()]  # Create a list of filters, removing whitespace

        if filters:  # If filters are specified
            filtered_items = [item for item in all_items if any(item.endswith(ext) for ext in filters)]  # Filter items based on extensions
        else:
            filtered_items = all_items  # If no filter is applied, show all items

        nonlocal total_pages  # Use nonlocal to modify the total_pages variable
        total_pages = math.ceil(len(filtered_items) / items_per_page)  # Recalculate total pages based on the filtered items
        current_page[0] = 1  # Reset to the first page
        update_tree(filtered_items)  # Update the Treeview with the filtered items

    # Create a frame to hold the filter entry and button
    filter_frame = tk.Frame(window)  # Frame for filter input
    filter_frame.pack(pady=10)  # Add padding around the filter frame

    # Entry widget for users to input file extensions for filtering
    filter_entry = tk.Entry(filter_frame, width=30, font=("Arial", 12))  # Input field for file extension filter
    filter_entry.pack(side=tk.LEFT, padx=5)  # Position the entry field in the filter frame

    # Button to apply the filter
    filter_button = tk.Button(filter_frame, text="Apply Filter", command=apply_filter, font=("Arial", 12, "bold"))  # Filter button
    filter_button.pack(side=tk.LEFT)  # Position the button next to the entry field

    # Function to create pagination buttons (First, Previous, Next, Last)
    def create_pagination_buttons(filtered_items):
        # Function to go to the previous page
        def go_previous():
            if current_page[0] > 1:  # Check if not on the first page
                current_page[0] -= 1  # Decrement the current page
                update_tree(filtered_items)  # Update the Treeview with the new page

        # Function to go to the next page
        def go_next():
            if current_page[0] < total_pages:  # Check if not on the last page
                current_page[0] += 1  # Increment the current page
                update_tree(filtered_items)  # Update the Treeview with the new page

        # Function to go to the first page
        def go_first():
            current_page[0] = 1  # Set current page to the first page
            update_tree(filtered_items)  # Update the Treeview with the first page

        # Function to go to the last page
        def go_last():
            current_page[0] = total_pages  # Set current page to the last page
            update_tree(filtered_items)  # Update the Treeview with the last page

        # Create a frame to hold pagination buttons
        btn_frame = tk.Frame(window)  # Frame for pagination buttons
        btn_frame.pack()  # Add the frame to the window

        # Button to go to the first page
        btn_first = tk.Button(btn_frame, text="First", command=go_first, font=("Arial", 10, "bold"))  # First page button
        btn_first.grid(row=0, column=0, padx=5)  # Position the button in the frame

        # Button to go to the previous page
        btn_previous = tk.Button(btn_frame, text="Previous", command=go_previous, font=("Arial", 10, "bold"))  # Previous page button
        btn_previous.grid(row=0, column=1, padx=5)  # Position the button in the frame

        # Button to go to the next page
        btn_next = tk.Button(btn_frame, text="Next", command=go_next, font=("Arial", 10, "bold"))  # Next page button
        btn_next.grid(row=0, column=2, padx=5)  # Position the button in the frame

        # Button to go to the last page
        btn_last = tk.Button(btn_frame, text="Last", command=go_last, font=("Arial", 10, "bold"))  # Last page button
        btn_last.grid(row=0, column=3, padx=5)  # Position the button in the frame

    # Initialize the Treeview by displaying the first page of all items
    update_tree(all_items)  # Update the Treeview with the first page of items
    create_pagination_buttons(all_items)  # Create the pagination buttons

    # Create an Exit button to close the application
    exit_button = tk.Button(window, text="Exit", command=window.quit, font=("Arial", 12, "bold"))  # Exit button
    exit_button.pack(pady=20)  # Add padding around the Exit button

# Main function to run the application
def main():
    root = tk.Tk()  # Create the main application window
    root.title("File Browser with Pagination")  # Set the window title
    root.geometry("600x500")  # Set the window size

    # Create a "Select Folder" button for the user to choose a folder
    select_button = tk.Button(root, text="Select Folder", command=lambda: select_folder(root), font=("Arial", 12, "bold"))
    select_button.pack(pady=20)  # Add padding around the Select Folder button

    root.mainloop()  # Start the main event loop for the application

# Call the main function to run the application
if __name__ == "__main__":
    main()  # Start the file browser application
