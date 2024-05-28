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

    # Show all folders with serial numbers
    print(Fore.CYAN + "Folders found inside 'folders' directory:" + Style.RESET_ALL)
    for i, folder in enumerate(folders, start=1):
        print(Fore.CYAN + f"{i}. {folder}" + Style.RESET_ALL)

    # Ask for serial number to delete
    while True:
        folder_sno = input(Fore.CYAN + "Enter the serial number of the folder you want to delete (0 to exit): " + Style.RESET_ALL)
        if folder_sno == "0":
            print(Fore.YELLOW + "Exiting without deleting any folder." + Style.RESET_ALL)
            break
        try:
            folder_sno = int(folder_sno)
            if folder_sno < 1 or folder_sno > len(folders):
                print(Fore.RED + "Invalid serial number. Please enter a valid serial number." + Style.RESET_ALL)
                continue
            folder_to_delete = folders[folder_sno - 1]
            folder_path = os.path.join(base_folder_path, folder_to_delete)

            # Ask user for confirmation to delete the folder
            delete_choice = input(Fore.CYAN + f"Do you want to delete the folder '{folder_to_delete}'? (yes/no): " + Style.RESET_ALL)
            if delete_choice.lower() == "yes":
                # Move the folder to the Recycle Bin
                send2trash(folder_path)
                print(Fore.GREEN + f"Folder '{folder_to_delete}' moved to Recycle Bin." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "Skipping deletion of this folder." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid serial number." + Style.RESET_ALL)

# Call the function to manage folders
manage_folders()
