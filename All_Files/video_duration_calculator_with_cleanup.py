# Import necessary libraries
import os  # for interacting with the file system
from moviepy.editor import VideoFileClip  # for getting the duration of video files
from tabulate import tabulate  # for formatting data into a table

# Function to handle cleanup after processing each video clip
def cleanup(clip):
    try:
        clip.close()  # Close the clip to release resources
    except Exception as e:
        print(f"Error during cleanup: {e}")


# Function to calculate the total duration of all video files in a given folder
def calculate_total_time(folder_path):
    video_data = []  # List to store data for each video file
    total_seconds = 0  # Initialize total duration in seconds
    total_files = 0  # Initialize total number of video files
    video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg']  # List of common video file extensions
    sno = 1  # Initialize serial number counter

    # Traverse through all files and subdirectories in the given folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.split('.')[-1].lower() in video_extensions:  # Check if the file is a video file
                file_path = os.path.join(root, file)  # Get the full path of the video file
                clip = VideoFileClip(file_path)  # Load the video clip
                try:
                    duration = clip.duration  # Get the duration of the video clip
                    total_seconds += duration  # Add the duration to the total duration
                    total_files += 1  # Increment the total number of video files

                    # Convert the duration to hours, minutes, and seconds
                    hours = int(duration // 3600)
                    minutes = int((duration % 3600) // 60)
                    seconds = int(duration % 60)

                    # Append data for the current video file to video_data list
                    video_data.append([sno, file, f"{hours} hours, {minutes} minutes, {seconds} seconds"])
                    sno += 1  # Increment serial number
                finally:
                    cleanup(clip)  # Call cleanup function to release resources after processing each video clip

    # Convert the total duration to hours, minutes, and seconds
    total_hours = int(total_seconds // 3600)
    total_minutes = int((total_seconds % 3600) // 60)
    total_seconds_remainder = int(total_seconds % 60)

    # Add a row for the total duration to the video_data list
    video_data.append(["Total", "", f"{total_hours} hours, {total_minutes} minutes, {total_seconds_remainder} seconds"])

    # Calculate the average duration
    if total_files != 0:
        average_duration_seconds = total_seconds / total_files
        average_minutes = int(average_duration_seconds // 60)
        average_seconds = int(average_duration_seconds % 60)
        average_duration_formatted = f"{average_minutes} minutes, {average_seconds} seconds"
    else:
        average_duration_formatted = "N/A"

    # Add a row for the average duration to the video_data list
    video_data.append(["Average", "", average_duration_formatted])

    # Define table headers
    table_headers = ["S.No", "Video File", "Duration"]

    # Print the formatted table using tabulate
    print("Total Duration of All Video Files:")
    print(tabulate(video_data, headers=table_headers, tablefmt="pretty"))


# Main function to prompt user for input and call the calculation functions
def main():
    path = input("Please enter the path to the directory containing video files: ")  # Ask user for folder path

    if not os.path.exists(path):  # Check if the entered path exists
        print("Invalid path!")  # Print error message if path is invalid
        return

    calculate_total_time(path)  # Calculate total duration


# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function
