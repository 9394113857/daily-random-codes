import os
import shutil
import time  # Import time module for sleep

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # Green color
    RED = '\033[91m'    # Red color
    END = '\033[0m'     # Reset style

def delete_item(item_path):
    """Attempt to delete a file or directory, with retries."""
    for _ in range(3):  # Retry up to 3 times
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)  # Delete the file
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Delete the directory and its contents
            print(Style.GREEN + f"Deleted: {item_path}" + Style.END)
            return True
        except PermissionError as e:
            print(Style.RED + f"PermissionError: {e} - Retrying in 2 seconds..." + Style.END)
            time.sleep(2)  # Wait for 2 seconds before retrying
        except Exception as e:
            print(Style.RED + f"Failed to delete {item_path}: {e} - Retrying in 2 seconds..." + Style.END)
            time.sleep(2)  # Wait for 2 seconds before retrying
    return False

def delete_percent_temp_items():
    # Path to the %temp% directory
    percent_temp_path = os.getenv('TMP')

    # List all files and directories in the %temp% directory
    contents = os.listdir(percent_temp_path)

    # Check if the %temp% directory is empty
    if not contents:
        print(Style.GREEN + "%temp% directory is already empty." + Style.END)
        return

    skipped_items = []  # List to keep track of skipped items

    # Delete all contents of the %temp% directory
    for item in contents:
        item_path = os.path.join(percent_temp_path, item)
        if not delete_item(item_path):
            print(Style.RED + f"Failed to delete {item_path} after multiple attempts." + Style.END)
            skipped_items.append(item_path)

    # Log skipped items
    if skipped_items:
        print(Style.RED + "\nThe following items could not be deleted as they are in use:" + Style.END)
        for item in skipped_items:
            print(Style.RED + item + Style.END)

    print(Style.RED + "\nCleanup process completed." + Style.END)

if __name__ == "__main__":
    delete_percent_temp_items()
