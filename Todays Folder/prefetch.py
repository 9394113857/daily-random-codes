import os
import shutil

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # Green color
    RED = '\033[91m'    # Red color
    END = '\033[0m'     # Reset style

def delete_prefetch_items():
    # Path to the Prefetch directory
    prefetch_path = os.path.join(os.getenv('SystemRoot'), r'Prefetch')

    # List all files in the Prefetch directory
    contents = os.listdir(prefetch_path)

    # Check if the Prefetch directory is empty
    if not contents:
        print(Style.GREEN + "Prefetch directory is already empty." + Style.END)
        return

    # Delete all contents of the Prefetch directory
    for item in contents:
        item_path = os.path.join(prefetch_path, item)
        # Check if the item is a file
        if os.path.isfile(item_path):
            os.remove(item_path)  # Delete the file
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)   # Delete the directory and its contents
    print(Style.RED + "All Prefetch items have been deleted." + Style.END)

if __name__ == "__main__":
    delete_prefetch_items()
