import os  # Importing the os module for interacting with the file system
import tkinter as tk  # Importing tkinter for GUI
from tkinter import ttk, messagebox, filedialog  # Importing additional tkinter components like Treeview, messagebox, and filedialog
import math  # Importing math for pagination calculations

# Function to handle folder selection and display its contents in a table format
def select_folder(window):
    folder_path = filedialog.askdirectory()  # Open folder selection dialog
    if folder_path:  # If the user selects a folder
        display_file_tree(window, folder_path)  # Display the file tree

# Function to display files in a table format with pagination
def display_file_tree(window, folder_path):
    # Clear the current window content
    for widget in window.winfo_children():
        widget.destroy()

    # Create a treeview widget for displaying files/folders in a tabular format
    tree = ttk.Treeview(window, columns=("S.No", "File/Folder"), show="headings")
    tree.heading("S.No", text="S.No")  # Set the heading for S.No column
    tree.heading("File/Folder", text="File/Folder")  # Set the heading for File/Folder column
    tree.pack(fill=tk.BOTH, expand=True)  # Expand it to fill the window space

    all_items = []  # List to hold all the items (files/folders)

    # Function to insert files/folders recursively in the tree
    def insert_files(parent, folder):
        try:
            # List directory content
            items = sorted(os.listdir(folder))  # Sorting directory items alphabetically
            for item in items:
                path = os.path.join(folder, item)  # Forming full path of the item
                all_items.append(item)  # Append the item to the list of all items
                if os.path.isdir(path):  # If the item is a folder
                    insert_files(parent, path)  # Recursively insert its contents
        except PermissionError:  # Catch permission errors (e.g., restricted folders)
            pass  # Ignore and move to the next item

    # Insert the root directory
    insert_files("", folder_path)  # Call the recursive function to insert files/folders

    # If the folder is empty, show an alert and provide feedback
    if not all_items:
        messagebox.showinfo("No Files Found", f"No files or folders found in {folder_path}")
        return  # Exit function if no items are found

    items_per_page = 10  # Define how many items to show per page
    current_page = [1]  # Use a list to allow modification in inner functions (mutable)
    total_pages = math.ceil(len(all_items) / items_per_page)  # Calculate total number of pages

    # Label to display the current page number and total pages
    page_label = tk.Label(window, text=f"Page {current_page[0]} of {total_pages}", font=("Arial", 12))  # Page label
    page_label.pack(pady=5)  # Add label with padding

    # Function to update the tree view based on the current page
    def update_tree(filtered_items):
        # Clear the tree (remove existing items)
        tree.delete(*tree.get_children())

        # Calculate the start and end index for the current page
        start = (current_page[0] - 1) * items_per_page  # Calculate start index
        end = min(start + items_per_page, len(filtered_items))  # Calculate end index (ensuring it doesn't exceed total items)

        # Insert the items for the current page with serial numbers
        for idx in range(start, end):  # Loop through items for the current page
            item = filtered_items[idx]  # Get the item from filtered list
            tree.insert("", "end", values=(idx + 1, item))  # Insert the item with its serial number

        # Update the page label to reflect current page and total pages
        page_label.config(text=f"Page {current_page[0]} of {total_pages}")  # Update page label text

    # Function to filter items based on the input extensions
    def apply_filter():
        filter_text = filter_entry.get()  # Get filter text from entry field
        # Split the input into a list of extensions and remove any whitespace
        filters = [ext.strip() for ext in filter_text.split(",") if ext.strip()]
        
        # Create a lambda function to check if the file ends with any of the specified extensions
        if filters:  # If there are filters specified
            filtered_items = [item for item in all_items if any(item.endswith(ext) for ext in filters)]
        else:
            filtered_items = all_items  # If no filters, show all items
        
        # Update total pages and reset to the first page
        total_pages = math.ceil(len(filtered_items) / items_per_page)  
        current_page[0] = 1  
        update_tree(filtered_items)  # Update the displayed items

    # Create a frame for the filter entry
    filter_frame = tk.Frame(window)  # Create a frame for the filter input
    filter_frame.pack(pady=10)  # Add the filter frame with padding

    # Entry for filter input
    filter_entry = tk.Entry(filter_frame, width=30, font=("Arial", 12))  # Create an entry field for filter input
    filter_entry.pack(side=tk.LEFT, padx=5)  # Position it in the frame

    # Filter button to apply the filter
    filter_button = tk.Button(filter_frame, text="Apply Filter", command=apply_filter, font=("Arial", 12, "bold"))  # Filter button
    filter_button.pack(side=tk.LEFT)  # Position it next to the entry

    # Add navigation buttons for pagination
    def create_pagination_buttons():
        # Previous button logic
        def go_previous(filtered_items):
            if current_page[0] > 1:  # If not on the first page
                current_page[0] -= 1  # Move to the previous page
                update_tree(filtered_items)  # Update tree view

        # Next button logic
        def go_next(filtered_items):
            if current_page[0] < total_pages:  # If not on the last page
                current_page[0] += 1  # Move to the next page
                update_tree(filtered_items)  # Update tree view

        # First page button logic
        def go_first(filtered_items):
            current_page[0] = 1  # Move to the first page
            update_tree(filtered_items)  # Update tree view

        # Last page button logic
        def go_last(filtered_items):
            current_page[0] = total_pages  # Move to the last page
            update_tree(filtered_items)  # Update tree view

        # Create buttons and bind to functions
        btn_frame = tk.Frame(window)  # Create a frame to hold buttons
        btn_frame.pack()  # Add the frame to the window

        btn_first = tk.Button(btn_frame, text="First", command=lambda: go_first(filtered_items), font=("Arial", 10, "bold"))  # First button
        btn_first.grid(row=0, column=0, padx=5)  # Position the First button

        btn_previous = tk.Button(btn_frame, text="Previous", command=lambda: go_previous(filtered_items), font=("Arial", 10, "bold"))  # Previous button
        btn_previous.grid(row=0, column=1, padx=5)  # Position the Previous button

        btn_next = tk.Button(btn_frame, text="Next", command=lambda: go_next(filtered_items), font=("Arial", 10, "bold"))  # Next button
        btn_next.grid(row=0, column=2, padx=5)  # Position the Next button

        btn_last = tk.Button(btn_frame, text="Last", command=lambda: go_last(filtered_items), font=("Arial", 10, "bold"))  # Last button
        btn_last.grid(row=0, column=3, padx=5)  # Position the Last button

    # Initialize the tree with the first page
    update_tree(all_items)  # Call update_tree to display the first page
    create_pagination_buttons()  # Add the pagination buttons

    # Create an Exit button
    exit_button = tk.Button(window, text="Exit", command=window.quit, font=("Arial", 12, "bold"))  # Exit button
    exit_button.pack(pady=20)  # Add the Exit button with padding

# Main function to create the Tkinter window
def main():
    window = tk.Tk()  # Create the main window
    window.title("File Tree Viewer")  # Set the window title
    window.geometry("600x400")  # Set window size

    # Add a label for the title
    label = tk.Label(window, text="File Tree Viewer", font=("Arial", 16, "bold"))  # Title label
    label.pack(pady=10)  # Add label with padding

    # Create a button to select a folder
    select_button = tk.Button(window, text="Select Folder", command=lambda: select_folder(window), font=("Arial", 12, "bold"))  # Button to select folder
    select_button.pack(pady=20)  # Add button with padding

    # Run the Tkinter event loop
    window.mainloop()  # Start the GUI

# Call the main function to run the program
if __name__ == "__main__":
    main()  # Entry point of the program
