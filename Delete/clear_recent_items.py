import os
import shutil

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # Green color for success messages
    RED = '\033[91m'    # Red color for error messages or empty state
    BLUE = '\033[94m'   # Blue color for user prompts
    BOLD = '\033[1m'    # Bold style for emphasis
    END = '\033[0m'     # Reset style to default

def delete_recent_items():
    # Path to the Recent Items directory in the user's AppData
    recent_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Recent')
    
    # File to track the status of the Recent Items directory
    status_file = "recent_items_status.txt"

    # List all files and directories in the Recent Items directory
    contents = os.listdir(recent_path)

    # Check if the Recent Items directory is empty
    if not contents:
        # Check if the status file exists and read its content
        if os.path.exists(status_file):
            with open(status_file, 'r') as file:
                status = file.read()
        else:
            status = ""

        # Determine the message based on the previous status
        if status == "empty":
            print(Style.RED + "The Recent Items directory is already empty." + Style.END)
        else:
            print(Style.GREEN + "The Recent Items directory is already empty." + Style.END)
        return

    # Prompt the user for confirmation to delete all recent items
    user_input = input(Style.BOLD + "Are you sure you want to delete all recent items? (yes/no): " + Style.END).lower()

    # If user confirms, proceed with deleting all contents
    if user_input == "yes":
        for item in contents:
            item_path = os.path.join(recent_path, item)
            # Check if the item is a file or directory
            if os.path.isfile(item_path):
                os.remove(item_path)  # Delete the file
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)   # Delete the directory and its contents
        
        # Update the status file to indicate that the directory was emptied
        with open(status_file, 'w') as file:
            file.write("empty")
        
        print(Style.GREEN + "All recent items have been deleted." + Style.END)
    elif user_input == "no":
        print(Style.BLUE + "Operation cancelled." + Style.END)
    else:
        print(Style.RED + "Invalid input. Operation cancelled." + Style.END)

if __name__ == "__main__":
    delete_recent_items()


"""
Comments Added:
1.	Imports: Importing necessary modules.
2.	Style Class: Defining ANSI escape codes for various colors and styles.
3.	Function Definition: delete_recent_items() handles the deletion of files in the Recent Items directory.
4.	Directory Path: Constructing the path to the Recent Items directory.
5.	Status File: Defining the file used to track the directory status.
6.	List Contents: Listing all items in the Recent Items directory.
7.	Check Empty Directory: Checking if the directory is empty and printing appropriate messages.
8.	Prompt User: Asking the user for confirmation to delete items.
9.	Delete Items: Deleting files and directories based on user confirmation.
10.	Update Status File: Updating the status file to reflect the empty state.
11.	Handle User Input: Handling different user inputs (confirmation or cancellation).
12.	Main Block: Calling the function when the script is run directly.
"""