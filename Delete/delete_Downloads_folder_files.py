import os
import shutil  # Import shutil module for rmtree function

# ANSI escape codes for colors
class Style:
    GREEN = '\033[92m'  # Green color for successful deletion
    RED = '\033[91m'    # Red color for already empty folder or errors
    BLUE = '\033[94m'   # Blue color for user prompts
    END = '\033[0m'     # Reset color

def delete_files_in_folder(folder_path):
    # Define the status file to keep track of the folder status
    status_file = "folder_status.txt"

    # Check if the provided folder path exists
    if not os.path.exists(folder_path):
        # If the folder path does not exist, print an error message and exit
        print(Style.RED + f"Error: The path '{folder_path}' does not exist. Please check the path and try again." + Style.END)
        return

    # List all files and directories in the given folder
    files_in_folder = os.listdir(folder_path)

    # Check if the folder is empty
    if not files_in_folder:
        # Check if the status file exists and read its content
        if os.path.exists(status_file):
            with open(status_file, 'r') as file:
                status = file.read()
        else:
            status = ""

        # Determine the message based on previous status
        if status == "deleted":
            print(Style.RED + "The folder is already empty." + Style.END)
        else:
            print(Style.RED + "The folder is already empty." + Style.END)
        return

    # Print the list of files in the folder
    print("Files in folder:")
    for file in files_in_folder:
        print(file)

    # Ask for confirmation before deleting all files
    confirmation = input(Style.BLUE + "Do you want to delete all files in this folder? (yes/no): " + Style.END)
    
    if confirmation.lower() == "yes":
        # Delete all files and directories in the folder
        for file in files_in_folder:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove the file if it's a file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Use shutil.rmtree() to delete non-empty directories
        
        # Update the status file to indicate that the folder was emptied
        with open(status_file, 'w') as file:
            file.write("deleted")
        
        # Print a success message
        print(Style.GREEN + "All files in the folder have been deleted." + Style.END)
    elif confirmation.lower() == "no":
        # If the user chooses not to delete, print a cancellation message
        print("Quitting the program.")
    else:
        # Handle invalid input
        print("Invalid input. Quitting the program.")

if __name__ == "__main__":
    while True:
        # Display options to the user
        print("Select the system:")
        print("1. Office")
        print("2. Laptop")
        print("3. Exit")  # Option to exit the program

        # Get user choice
        system_choice = input("Enter the number corresponding to your choice (1, 2, or 3): ")

        # Exit the program if the user selects option 3
        if system_choice == "3":
            print(Style.BLUE + "Exiting the program. Goodbye!" + Style.END)
            break
        
        # Define folder paths based on user choice
        if system_choice == "1":
            folder_path = r"C:\Users\pc\Downloads"  # Path for office system
        elif system_choice == "2":
            folder_path = r"C:\Users\your-laptop-username\Downloads"  # Replace with actual laptop path
        else:
            # Handle invalid system choice
            print(Style.RED + "Invalid system choice. Please select a valid option." + Style.END)
            continue

        # Call the function to delete files in the selected folder
        delete_files_in_folder(folder_path)

""" 
Comments Added:
1.	Imports: Importing necessary modules (os and shutil).
2.	Style Class: Defining ANSI escape codes for different colors and styles.
3.	Function Definition: delete_files_in_folder() handles the deletion of files in a specified folder.
4.	Folder Path Check: Verifying if the provided folder path exists; if not, print an error message and exit.
5.	List Files: Listing all files and directories in the specified folder.
6.	Check Empty Folder: Checking if the folder is empty and reading the status file if it exists.
7.	Empty Folder Message: Displaying a message if the folder is already empty based on the status.
8.	File Deletion: Asking for user confirmation before deleting files and directories.
9.	Delete Files: Deleting files and directories based on user input and updating the status file.
10.	User Input Handling: Managing user responses for deletion or cancellation.
11.	Main Block: Providing options to the user, including the option to exit, and handling invalid choices.
"""