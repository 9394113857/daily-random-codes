import os
from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize colorama
init()

# Function to calculate the size of a directory
def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

# Function to calculate and display the sizes of subdirectories
def calculate_folder_sizes(root_folder):
    subfolder_sizes = []

    # Traverse each subdirectory in the root folder
    for subdir in os.listdir(root_folder):
        subdir_path = os.path.join(root_folder, subdir)
        if os.path.isdir(subdir_path):
            subdir_size = get_directory_size(subdir_path)
            subfolder_sizes.append((subdir, f"{subdir_size / (1024 * 1024):.2f} MB"))
            print(Fore.GREEN + f"Size of folder '{subdir}': {subdir_size / (1024 * 1024):.2f} MB" + Style.RESET_ALL)

    # Calculate the total size
    total_size = sum(float(size.split()[0]) for _, size in subfolder_sizes)
    subfolder_sizes.append(("Total size of all folders", f"{total_size:.2f} MB"))

    # Print the folder sizes in tabulated form
    table = tabulate(subfolder_sizes, headers=["Folder Name", "Size"], tablefmt="grid")
    print(Fore.CYAN + table + Style.RESET_ALL)

# Call the function to calculate and display the folder sizes
if __name__ == "__main__":
    # Define the root folder
    root_folder = 'folders'  # You can change this to the path you want

    # Check if the root folder exists
    if os.path.exists(root_folder) and os.path.isdir(root_folder):
        calculate_folder_sizes(root_folder)
    else:
        print(Fore.RED + "The specified root folder does not exist or is not a directory." + Style.RESET_ALL)
