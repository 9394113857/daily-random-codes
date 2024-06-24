import os

# Define the path
path = r"C:\Users\pc\Desktop\Inv - Quality Healthcare\May 2024 changes saved only"

# Define the suffix to add
suffix = "_2024-25"

# Counters for renamed and skipped files
renamed_count = 0
skipped_count = 0

# Iterate through files in the directory
for filename in os.listdir(path):
    if filename.endswith(".pdf"):
        # Full file path
        full_path = os.path.join(path, filename)
        
        # Check if the suffix is already applied
        if filename.endswith(f"{suffix}.pdf"):
            print(f"Already applied, skipping: {filename}")
            skipped_count += 1
        else:
            # Get the file name without extension
            base_name = os.path.splitext(filename)[0]
            
            # New file name with the suffix
            new_name = base_name + suffix + ".pdf"
            new_full_path = os.path.join(path, new_name)
            
            # Rename the file
            os.rename(full_path, new_full_path)
            print(f"Renamed: {filename} to {new_name}")
            renamed_count += 1

# Print summary
print(f"Total files renamed: {renamed_count}")
print(f"Total files skipped: {skipped_count}")
