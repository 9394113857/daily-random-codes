import os


def delete_files_except_jpeg_jpg(directory):
    extra_files_deleted = False
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            # Check if the file is not a .jpeg or .jpg file
            if not filename.lower().endswith(('.jpeg', '.jpg')):
                os.remove(filepath)
                print(f"Deleted: {filename}")
                extra_files_deleted = True
    if not extra_files_deleted:
        print("No extra files found. Skipping deletion.")


# Ask the user to input the directory path
directory_path = input("Enter the directory path: ")

# Check if the directory path is valid
if os.path.isdir(directory_path):
    # Call the function to delete files except .jpeg and .jpg
    delete_files_except_jpeg_jpg(directory_path)
else:
    print("Invalid directory path.")
