import os
import shutil
from colorama import init, Fore, Style

# Initialize colorama
init()

# Function to get folder size
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Function to list folders and their sizes
def list_folders():
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

    # Print table header
    print(Fore.CYAN + f"{'S.No':<5} {'Folder Name':<30} {'Folder Size (MB)':<20}" + Style.RESET_ALL)

    # Print folders and their sizes
    for i, folder in enumerate(folders, start=1):
        folder_path = os.path.join(base_folder_path, folder)
        folder_size_mb = get_folder_size(folder_path) / (1024 * 1024)  # Convert folder size to MB
        print(f"{i:<5} {folder:<30} {folder_size_mb:.2f} MB")

# Call the function to list folders and their sizes
list_folders()
