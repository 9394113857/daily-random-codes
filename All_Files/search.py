import os


def search_files(search_path, search_item):
    found_files = []
    for root, _, files in os.walk(search_path):
        for file in files:
            if search_item.lower() in file.lower():
                found_files.append(os.path.join(root, file))
    return found_files


def main():
    while True:
        drive_path = input("Please enter the drive path (e.g., D:\\): ")
        search_item = input("Please enter the file extension or file name to search for (e.g., .py or example.txt): ")
        if not os.path.exists(drive_path):
            print("Invalid drive path. Please try again.")
            continue

        found_files = search_files(drive_path, search_item)
        if found_files:
            print("\nYes, I found the following files:\n")
            for found_file in found_files:
                print(found_file)
        else:
            print(f"Sorry, no files matching '{search_item}' found in {drive_path}.")

        choice = input("\nWould you like to continue searching? (yes/no): ")
        if choice.lower() != 'yes':
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
