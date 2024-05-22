import os
import shutil

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # Green color
    RED = '\033[91m'    # Red color
    BLUE = '\033[94m'   # Blue color
    BOLD = '\033[1m'    # Bold style
    END = '\033[0m'     # Reset style

def delete_downloads_contents():
    # Path to the Downloads directory
    downloads_path = r'C:\Users\pc\Downloads'

    # List all files and directories in the Downloads directory
    contents = os.listdir(downloads_path)

    # Check if the Downloads directory is empty
    if not contents:
        print(Style.GREEN + "Downloads directory is already empty." + Style.END)
        return

    # Prompt the user for confirmation
    user_input = input(Style.BOLD + "Are you sure you want to delete all contents of the Downloads directory? (yes/no): " + Style.END).lower()

    # If user confirms, proceed with deleting all contents
    if user_input == "yes":
        for item in contents:
            item_path = os.path.join(downloads_path, item)
            # Check if the item is a file or directory
            if os.path.isfile(item_path):
                os.remove(item_path)  # Delete the file
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)   # Delete the directory and its contents
        print(Style.RED + "All contents in Downloads directory have been deleted." + Style.END)
    elif user_input == "no":
        print(Style.BLUE + "Operation cancelled." + Style.END)
    else:
        print(Style.RED + "Invalid input. Operation cancelled." + Style.END)

if __name__ == "__main__":
    delete_downloads_contents()
