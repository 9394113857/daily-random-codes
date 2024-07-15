import os
import re
import datetime

def rename_files(directory_path):
    # List all files in the directory
    files = os.listdir(directory_path)

    # Filter out only the PDF files
    pdf_files = [file for file in files if file.endswith('.pdf')]

    # Check if there are more than 40 files
    if len(pdf_files) <= 40:
        print("There are not enough files to rename.")
        return

    # Sort the files
    pdf_files.sort()

    # Initialize counter for processed files
    files_processed = 0

    # Generate the new filenames and rename the files
    for i, file in enumerate(pdf_files):
        new_filename = f"QM-{str(i+197).zfill(4)}_{datetime.datetime.now().strftime('%Y-%m')}.pdf"
        old_filepath = os.path.join(directory_path, file)
        new_filepath = os.path.join(directory_path, new_filename)

        try:
            # Rename the file
            os.rename(old_filepath, new_filepath)
            # Print status
            print(f"{file} renamed as {new_filename}")
            files_processed += 1
        except Exception as e:
            # If any error occurs during file renaming, print the error message
            print(f"Error occurred while renaming {file}: {str(e)}")

    # Print the total number of files processed
    print(f"\nTotal files processed: {files_processed}")

# Example usage
directory_path = r"C:\Users\pc\Desktop\Inv - Quality Medicare"
rename_files(directory_path)
