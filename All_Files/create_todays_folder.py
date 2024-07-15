import os
from datetime import datetime

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m' 

# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):  # Check if the folder does not exist
        os.makedirs(folder_path)  # Create the folder and any necessary parent folders
        print(Style.BOLD + Style.GREEN + "Folder created successfully." + Style.END)  # Print success message in bold green
        return folder_path  # Return the path of the created folder
    else:
        print(Style.BOLD + Style.RED + "Folder already exists." + Style.END)  # Print message indicating that folder already exists in bold red
        return folder_path  # Return the path of the existing folder


# Main function
def main():
    # Path to the parent directory
    parent_directory = r'C:\Users\pc\Downloads'

    # Get today's date
    today_date = datetime.today().strftime('%d-%m-%y')

    # Path to the folder
    folder_path = os.path.join(parent_directory, today_date)

    # Create folder if it doesn't exist
    created_folder = create_folder_if_not_exists(folder_path)

    # Get the current date and time
    creation_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Display the created folder name, path, and creation datetime
    folder_name = os.path.basename(created_folder)
    print(Style.BOLD + "Created folder name:" + Style.END, folder_name)  # Print the name of the created folder in bold
    print(Style.BOLD + "Created folder path:" + Style.END, created_folder)  # Print the path of the created folder in bold
    print(Style.BOLD + "Creation date and time:" + Style.END, Style.BOLD + Style.BLUE + today_date + Style.END)  # Print the creation date and time in bold and blue


if __name__ == "__main__":
    main()
