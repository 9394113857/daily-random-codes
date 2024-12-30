import os

def rename_files_in_directory(path):
    try:
        # Check if the provided path is a directory
        if not os.path.isdir(path):
            print(f"The path '{path}' is not a valid directory. Please check and try again.")
            return

        # List all PDF files that start with 'H-'
        files = [f for f in os.listdir(path) if f.startswith('H-') and f.endswith('.pdf')]

        # Check if any matching files exist
        if not files:
            print("No files matching 'H-*.pdf' found in the directory.")
            return

        # Confirm processing with the user
        proceed = input("Files detected. Do you want to process them? (yes/no): ").strip().lower()
        if proceed != 'yes':
            print("Process cancelled.")
            return

        # Rename files
        for f in files:
            old_file_path = os.path.join(path, f)
            new_file_name = f"Q{f[1:]}"  # Remove 'H' and add 'Q' at the start
            new_file_path = os.path.join(path, new_file_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{f}' to '{new_file_name}'")

        print("Renaming process completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Get user input for the directory path
    user_input_path = input("Please enter the directory path: ").strip()
    rename_files_in_directory(user_input_path)

if __name__ == "__main__":
    main()
