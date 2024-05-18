import os
import shutil
import time

def clear_directory(directory):
    """
    Clear all files and subdirectories inside the specified directory.
    """
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        try:
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Failed to delete {item_path}: {e}")
            # Wait for a short duration and retry
            time.sleep(1)
            try:
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                print(f"Deleted {item_path} successfully after retry.")
            except Exception as e:
                print(f"Failed to delete {item_path} after retry: {e}")

def main():
    # List of directories to clear
    directories = ['C:\\Windows\\Recent', 'C:\\Windows\\Temp', os.environ['TEMP']]

    # Loop through directories and clear them
    for directory in directories:
        if directory == os.environ['TEMP']:
            directory = os.path.abspath(directory)  # Resolves the environment variable path
        if os.path.exists(directory):
            try:
                clear_directory(directory)
                print(f"Cleared {directory} successfully.")
            except Exception as e:
                print(f"Failed to clear {directory}: {e}")
        else:
            print(f"Directory {directory} does not exist.")

if __name__ == "__main__":
    main()
