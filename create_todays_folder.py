import os
from datetime import datetime


# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):  # Check if the folder does not exist
        os.makedirs(folder_path)  # Create the folder and any necessary parent folders
        print("Folder created successfully.")  # Print success message
        return folder_path  # Return the path of the created folder
    else:
        print("Folder already exists.")  # Print message indicating that folder already exists
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
    print("Created folder name:", folder_name)  # Print the name of the created folder
    print("Created folder path:", created_folder)  # Print the path of the created folder
    print("Creation date and time:", creation_datetime)  # Print the creation date and time


if __name__ == "__main__":
    main()
