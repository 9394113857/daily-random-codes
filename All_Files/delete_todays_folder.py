import os
from datetime import datetime

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

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
            os.rmdir(folder_path)  # Remove the directory
            print(Style.BOLD + Style.RED + "Folder deleted successfully." + Style.END)  # Print success message in bold red
        except OSError as e:
            print(Style.BOLD + Style.RED + "Error: %s : %s" % (folder_path, e.strerror) + Style.END)  # Print error message in bold red
    else:
        print(Style.BOLD + Style.RED + "Folder does not exist." + Style.END)  # Print message indicating that folder does not exist in bold red


if __name__ == "__main__":
    main()
