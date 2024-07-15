import os
import shutil  # Import shutil module for rmtree function

def delete_files_in_folder(folder_path):
    # List all files and directories in the given folder
    files_in_folder = os.listdir(folder_path)
    
    # If the folder is empty, print a message and return
    if not files_in_folder:
        print("The folder is already empty.")
        return
    
    # Print the list of files in the folder
    print("Files in folder:")
    for file in files_in_folder:
        print(file)
    
    # Ask for confirmation before deleting
    confirmation = input("Do you want to delete all files in this folder? (yes/no): ")
    
    if confirmation.lower() == "yes":
        # Delete all files in the folder
        for file in files_in_folder:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove the file if it's a file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Use shutil.rmtree() to delete non-empty directories
        print("All files in the folder have been deleted.")
    elif confirmation.lower() == "no":
        print("Quitting the program.")
    else:
        print("Invalid input. Quitting the program.")

if __name__ == "__main__":
    # Define the folder path
    folder_path = r"C:\Users\pc\Downloads"
    # Call the function to delete files in the folder
    delete_files_in_folder(folder_path)
