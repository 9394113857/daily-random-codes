import os
import shutil

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # Green color
    RED = '\033[91m'    # Red color
    BLUE = '\033[94m'   # Blue color
    BOLD = '\033[1m'    # Bold style
    END = '\033[0m'     # Reset style

def delete_recent_items():
    # Path to the Recent Items directory
    recent_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Recent')

    # List all files and directories in the Recent Items directory
    contents = os.listdir(recent_path)

    # Check if the Recent Items directory is empty
    if not contents:
        print(Style.GREEN + "Recent Items directory is already empty." + Style.END)
        return

    # Prompt the user for confirmation
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
        print(Style.RED + "All recent items have been deleted." + Style.END)
    elif user_input == "no":
        print(Style.BLUE + "Operation cancelled." + Style.END)
    else:
        print(Style.RED + "Invalid input. Operation cancelled." + Style.END)

if __name__ == "__main__":
    delete_recent_items()
