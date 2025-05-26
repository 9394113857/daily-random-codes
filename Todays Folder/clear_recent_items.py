import os            # Import the os module to interact with the operating system
import shutil        # Import the shutil module to perform file operations (like deleting directories)

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # Green color for positive messages
    RED = '\033[91m'    # Red color for error or delete messages
    BLUE = '\033[94m'   # Blue color for informational messages
    BOLD = '\033[1m'    # Bold text for emphasis
    END = '\033[0m'     # Reset style to normal

def delete_recent_items():
    # Path to the "Recent Items" folder in the current user's AppData
    recent_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Recent')

    # List all files and directories in the Recent Items directory
    contents = os.listdir(recent_path)

    # Check if the Recent Items directory is empty
    if not contents:
        print(Style.GREEN + "Recent Items directory is already empty." + Style.END)  # Display a message if empty
        return  # Exit the function if the directory is already empty

    # Proceed with deleting all contents without asking for user confirmation
    for item in contents:  # Iterate over each file or directory in the Recent Items folder
        item_path = os.path.join(recent_path, item)  # Get the full path of each item

        # Check if the item is a file (and delete it if it is)
        if os.path.isfile(item_path):
            os.remove(item_path)  # Delete the file
        # Check if the item is a directory (and delete it and its contents if it is)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Delete the directory and its contents

    # Once the deletion is complete, display a message
    print(Style.RED + "All recent items have been deleted." + Style.END)

if __name__ == "__main__":
    delete_recent_items()  # Call the function to delete all recent items
