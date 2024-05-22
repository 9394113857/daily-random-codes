import os
import shutil
from send2trash import send2trash
from colorama import init, Fore, Style

# Initialize colorama
init()

# Function to list and possibly delete folders inside the "folders" directory
def manage_folders():
    # Ensure the "folders" directory exists
    base_folder_path = os.path.join(os.getcwd(), "folders")
    if not os.path.exists(base_folder_path):
        print(Fore.YELLOW + f"The directory '{base_folder_path}' does not exist." + Style.RESET_ALL)
        return

    # List all folders inside the "folders" directory
    folders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]
    
    if not folders:
        print(Fore.YELLOW + "No folders found inside 'folders' directory." + Style.RESET_ALL)
        return

    # Iterate through each folder and ask the user if they want to delete it
    for folder in folders:
        folder_path = os.path.join(base_folder_path, folder)
        print(Fore.CYAN + f"Folder: {folder}" + Style.RESET_ALL)

        # Ask user if they want to delete the folder
        delete_choice = input(Fore.CYAN + f"Do you want to delete the folder '{folder}'? (yes/no): " + Style.RESET_ALL)
        if delete_choice.lower() == "yes":
            # Move the folder to the Recycle Bin
            send2trash(folder_path)
            print(Fore.GREEN + f"Folder '{folder}' moved to Recycle Bin." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Exiting without deleting any more folders." + Style.RESET_ALL)
            break

# Call the function to manage folders
manage_folders()
