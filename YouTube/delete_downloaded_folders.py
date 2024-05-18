import os
import shutil

# Function to list and possibly delete folders inside the "folders" directory
def manage_folders():
    # Ensure the "folders" directory exists
    base_folder_path = os.path.join(os.getcwd(), "folders")
    if not os.path.exists(base_folder_path):
        print(f"The directory '{base_folder_path}' does not exist.")
        return

    # List all folders inside the "folders" directory
    folders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]
    
    if not folders:
        print("No folders found inside 'folders' directory.")
        return

    # Iterate through each folder and ask the user if they want to delete it
    for folder in folders:
        folder_path = os.path.join(base_folder_path, folder)
        print(f"Folder: {folder}")

        # Ask user if they want to delete the folder
        delete_choice = input(f"Do you want to delete the folder '{folder}'? (yes/no): ")
        if delete_choice.lower() == "yes":
            # Delete the folder
            shutil.rmtree(folder_path)
            print(f"Folder '{folder}' deleted.")
        else:
            print("Exiting without deleting any more folders.")
            break

# Call the function to manage folders
manage_folders()
