import os
import shutil

# ANSI escape codes for colors and styles
class Style:
    GREEN = '\033[92m'  # Green color
    RED = '\033[91m'    # Red color
    BLUE = '\033[94m'   # Blue color
    BOLD = '\033[1m'    # Bold style
    END = '\033[0m'     # Reset style

def delete_selected_contents(directory_path):
    # List all files and directories in the specified directory
    try:
        contents = os.listdir(directory_path)
    except FileNotFoundError:
        print(Style.RED + "The specified directory does not exist." + Style.END)
        return
    except PermissionError:
        print(Style.RED + "You do not have permission to access this directory." + Style.END)
        return

    # Check if the directory is empty
    if not contents:
        print(Style.GREEN + "The directory is already empty." + Style.END)
        return

    # Display the contents with indices
    print(Style.BOLD + "Contents of the directory:" + Style.END)
    for idx, item in enumerate(contents, start=1):
        print(f"{idx}. {item}")

    # Prompt the user to select items to delete
    user_input = input(Style.BOLD + "Enter the numbers of the items you want to delete, separated by commas (e.g., 1,3,5): " + Style.END).split(',')

    # Parse the user input to get indices
    try:
        indices_to_delete = [int(num.strip()) for num in user_input if num.strip().isdigit()]
    except ValueError:
        print(Style.RED + "Invalid input. Please enter numbers only." + Style.END)
        return

    # Validate indices
    if not indices_to_delete or any(idx < 1 or idx > len(contents) for idx in indices_to_delete):
        print(Style.RED + "Invalid input. Please enter valid item numbers." + Style.END)
        return

    # Confirm the deletion
    items_to_delete = [contents[idx - 1] for idx in indices_to_delete]
    print(Style.BOLD + "You have selected the following items for deletion:" + Style.END)
    for item in items_to_delete:
        print(f"- {item}")

    final_confirmation = input(Style.BOLD + "Are you sure you want to delete the selected items? (yes/no): " + Style.END).lower()

    # If user confirms, proceed with deleting the selected items
    if final_confirmation == "yes":
        for item in items_to_delete:
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)  # Delete the file
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Delete the directory and its contents
        print(Style.RED + "Selected items have been deleted." + Style.END)
    elif final_confirmation == "no":
        print(Style.BLUE + "Operation cancelled." + Style.END)
    else:
        print(Style.RED + "Invalid input. Operation cancelled." + Style.END)

if __name__ == "__main__":
    # Prompt the user to enter the path to the directory
    directory_path = input(Style.BOLD + "Enter the path to the directory you want to clean up: " + Style.END)
    delete_selected_contents(directory_path)
