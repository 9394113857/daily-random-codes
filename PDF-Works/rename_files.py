import os

# Define the directory path
folder_path = r"C:\Users\pc\Desktop\Inv - Quality Healthcare\Nov-2024"

# Initialize counters for different actions
deleted_count = 0
renamed_count = 0
skipped_count = 0
created_count = 0
addon_count = 0  # This could track if the file already exists and we try to add suffixes (optional)

# Loop through all files in the directory
for filename in os.listdir(folder_path):
    # Check if the file matches the pattern
    if filename.endswith(".pdf") and filename.startswith("QH-"):
        # Split the filename into parts based on underscores
        parts = filename.split("_")
        
        # Check if this file has the exact format "QH-<number>.pdf"
        if len(parts) == 2:  # Format: QH-<number>.pdf
            base_filename = parts[0] + "_" + parts[1]
            new_filename = base_filename + "_2024-25.pdf"
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            # Check if the "_2024-25" version of the file exists
            if os.path.exists(new_file_path):
                # Delete the older version (without "_2024-25")
                os.remove(old_file_path)
                deleted_count += 1
                print(f"Deleted: {old_file_path} (because corresponding {new_filename} exists)")

        # If there's an extra numeric part like "_001"
        elif len(parts) > 2 and parts[-1].isdigit():  # Format: QH-<number>_2024-25_001.pdf
            new_filename = "_".join(parts[:-1]) + ".pdf"  # Remove the last numeric part
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            # Check if the target file already exists
            if os.path.exists(new_file_path):
                # Skip the rename if the file already exists
                skipped_count += 1
                print(f"File already exists, skipping rename: {new_file_path}")
            else:
                # Rename to the desired format
                os.rename(old_file_path, new_file_path)
                renamed_count += 1
                print(f"Renamed: {old_file_path} to {new_file_path}")
        
        else:
            # If the file is already in the correct format, just rename if needed
            new_filename = "_".join(parts[:-1]) + ".pdf"
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            # Check if the target file already exists
            if os.path.exists(new_file_path):
                # Skip the rename if the file already exists
                skipped_count += 1
                print(f"File already exists, skipping rename: {new_file_path}")
            else:
                os.rename(old_file_path, new_file_path)
                renamed_count += 1
                print(f"Renamed: {old_file_path} to {new_file_path}")

# Summary of actions
print("\nSummary of actions:")
print(f"Total files deleted: {deleted_count}")
print(f"Total files renamed: {renamed_count}")
print(f"Total files skipped (already exists): {skipped_count}")
print(f"Total files created (new names): {created_count}")
print(f"Total files with added suffix (if any): {addon_count}")
