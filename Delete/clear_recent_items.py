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

    # Delete all contents in the Recent Items directory without asking for confirmation
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

if __name__ == "__main__":
    delete_recent_items()
