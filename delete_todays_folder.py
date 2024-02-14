import os
from datetime import datetime

def delete_folder_if_exists(folder_path):
    if os.path.exists(folder_path):  # Check if the folder exists
        os.rmdir(folder_path)  # Delete the folder
        print("Folder deleted successfully.")  # Print success message
        return folder_path  # Return the path of the deleted folder
    else:
        print("Folder does not exist.")  # Print message indicating that folder does not exist
        return None  # Return None if the folder does not exist

def main():
    # Path to the parent directory
    parent_directory = r'C:\Users\pc\Downloads'

    # Get today's date
    today_date = datetime.today().strftime('%d-%m-%y')

    # Path to the folder
    folder_path = os.path.join(parent_directory, today_date)

    # Delete folder if it exists
    deleted_folder = delete_folder_if_exists(folder_path)

    # Get the current date and time
    deletion_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if deleted_folder:
        # Display the deleted folder path and deletion datetime
        print("Deleted folder path:", deleted_folder)
        print("Deletion date and time:", deletion_datetime)


if __name__ == "__main__":
    main()
