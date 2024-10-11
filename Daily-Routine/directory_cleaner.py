import os
import shutil
import logging
from tkinter import Tk, filedialog, messagebox, Button, Label  # Import tkinter modules for the GUI
from pathlib import Path  # Import Path for handling paths easily
import send2trash  # Import send2trash to send files to the recycle bin
from tabulate import tabulate  # Import tabulate to create table views for file preview
from datetime import datetime  # Import datetime to handle time-related tasks

# Set up logging to automatically create a log file inside year/month folder structure
def setup_logging():
    # Create logs folder structure: logs/year/month
    logs_folder = os.path.join("logs", datetime.now().strftime("%Y"), datetime.now().strftime("%m"))
    os.makedirs(logs_folder, exist_ok=True)  # Make the folders if they don't exist
    # Create a log file name based on the current date
    log_file = os.path.join(logs_folder, f"{datetime.now().strftime('%d-%m-%Y')}_deletion.log")
    # Set up logging configuration
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Function to fix the path provided by the user
def fix_path(user_path):
    # Normalize the path to handle slashes, and get absolute path
    fixed_path = os.path.normpath(user_path)
    fixed_path = str(Path(fixed_path).resolve())  # Resolve to get absolute path
    return fixed_path  # Return the corrected path

# Function to delete contents inside the directory
def delete_contents(directory):
    try:
        # Normalize and fix the directory path
        directory = fix_path(directory)
        logging.info(f"Directory after fixing: {directory}")  # Log the fixed path
        
        # Check if the directory exists
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist.")  # Raise an error if the directory doesn't exist
        
        # Get the list of all files/folders inside the directory
        items = os.listdir(directory)  # List all files/folders in the directory
        file_list = []  # List to store files/folders details for preview
        
        # Enumerate through all items and categorize them as File or Folder
        for index, item in enumerate(items, start=1):
            item_path = os.path.join(directory, item)
            file_list.append([index, item, 'File' if os.path.isfile(item_path) else 'Folder'])

        # Show file list preview in a table format using tabulate
        table = tabulate(file_list, headers=["S.No", "Name", "Type"], tablefmt="fancy_grid")
        logging.info(f"Files and folders inside {directory}:\n{table}")  # Log the list of files/folders
        print(f"Preview of files/folders inside {directory}:\n{table}")  # Print the preview to the console

        # Ask for user confirmation to proceed with deletion
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete all the contents in {directory}?")

        if confirmation:
            # Delete all contents in the directory if the user confirms
            for item in items:
                item_path = os.path.join(directory, item)
                item_path = os.path.normpath(item_path)  # Ensure path is fixed
                
                if os.path.exists(item_path):  # Check if the path exists before deleting
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        send2trash.send2trash(item_path)  # Send file/link to recycle bin
                        os.remove(item_path)  # Permanently remove the file
                    elif os.path.isdir(item_path):
                        send2trash.send2trash(item_path)  # Send folder to recycle bin
                        shutil.rmtree(item_path)  # Permanently remove the folder

            # Log and show success message
            logging.info(f"All contents deleted successfully from {directory}.")
            messagebox.showinfo("Success", "All contents have been deleted successfully!")
        else:
            # If user cancels, log and show cancellation message
            logging.info("Deletion canceled by user.")
            messagebox.showinfo("Canceled", "Deletion has been canceled.")
    except FileNotFoundError as fnfe:
        # Handle the case where the directory is not found
        logging.error(f"Error: {fnfe}")
        messagebox.showerror("Error", f"Error: {fnfe}")
    except Exception as e:
        # Catch any other exceptions that may occur
        logging.error(f"Error deleting contents: {e}")
        messagebox.showerror("Error", f"Error deleting contents: {e}")

# Function to take user input for directory path and validate it
def select_directory():
    root = Tk()  # Initialize tkinter window
    root.withdraw()  # Hide the main window (so only file dialog is shown)
    user_path = filedialog.askdirectory(title="Select a Directory")  # Show directory selection dialog
    
    if user_path:
        # Fix the user path immediately after input
        fixed_path = fix_path(user_path)
        logging.info(f"User selected path: {user_path}")  # Log the raw path from user input
        logging.info(f"Fixed path: {fixed_path}")  # Log the fixed/normalized path
        
        # Show the fixed path to the user in a messagebox
        messagebox.showinfo("Selected Path", f"Final path: {fixed_path}")
        
        # Proceed to delete contents inside the fixed path
        delete_contents(fixed_path)
    else:
        # If no directory is selected, log the warning and show a message
        logging.info("No directory selected.")
        messagebox.showwarning("Warning", "No directory selected. Please select a directory.")

# Function to create the UI using tkinter
def create_ui():
    root = Tk()  # Initialize the tkinter window
    root.title("Directory Content Deletion")  # Set the window title
    root.geometry("400x300")  # Set the window size

    # Add a label to the window
    Label(root, text="Select Directory and Delete Contents", font=("Arial", 14, "bold")).pack(pady=20)

    # Add a button for selecting the directory
    select_button = Button(root, text="Select Directory", command=select_directory, font=("Arial", 12))
    select_button.pack(pady=10)

    # Add a big exit button at the bottom
    exit_button = Button(root, text="Exit", command=root.quit, font=("Arial", 12), fg="white", bg="red")
    exit_button.pack(pady=40)

    root.mainloop()  # Start the tkinter event loop to display the window

# Main function: set up logging and create the UI
if __name__ == "__main__":
    setup_logging()  # Set up logging for the application
    create_ui()  # Launch the UI
