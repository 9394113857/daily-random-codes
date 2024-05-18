import os  # Importing the os module for file system operations
import shutil  # Importing the shutil module for high-level file operations
from datetime import datetime  # Importing datetime class from the datetime module

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # ANSI escape code for green color
    RED = '\033[91m'    # ANSI escape code for red color
    BLUE = '\033[94m'   # ANSI escape code for blue color
    BOLD = '\033[1m'    # ANSI escape code for bold style
    END = '\033[0m'     # ANSI escape code to reset style

# Main function
def main():
    # Path to the parent directory
    parent_directory = r'C:\Users\pc\Downloads'

    # Get today's date
    today_date = datetime.today().strftime('%d-%m-%y')

    # Path to the folder
    folder_path = os.path.join(parent_directory, today_date)

    # Check if the folder exists 
    if os.path.exists(folder_path):
        # Deleting today's folder
        try:
            shutil.rmtree(folder_path)  # Remove the directory and its contents
            print(Style.BOLD + Style.RED + "Folder deleted successfully." + Style.END)  # Print success message in bold red
        except OSError as e:
            print(Style.BOLD + Style.RED + "Error: %s : %s" % (folder_path, e.strerror) + Style.END)  # Print error message in bold red
    else:
        print(Style.BOLD + Style.RED + "Folder does not exist." + Style.END)  # Print message indicating that folder does not exist in bold red


if __name__ == "__main__":
    main()  # Call the main function if the script is executed directly
