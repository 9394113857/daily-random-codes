# Filename: download_youtube_channel_videos.py

# Import necessary libraries
from pytube import Channel  # Import Channel class from pytube module for downloading YouTube channel videos
import os  # Import os module for interacting with the operating system
import shutil  # Import shutil module for high-level file operations
from colorama import init, Fore, Style  # Import colorama for colored terminal output
from pytube.exceptions import AgeRestrictedError  # Import specific exception for age-restricted videos

# Initialize colorama to support colored terminal output
init()

# Function to get folder size
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):  # Walk through each file and subdirectory in the folder
        for f in filenames:  # Iterate through files
            fp = os.path.join(dirpath, f)  # Get the full path of the file
            total_size += os.path.getsize(fp)  # Add the size of the file to total_size
    return total_size  # Return the total size of the folder in bytes

# Function to download channel videos and organize into folder
def download_channel_videos():
    # Ensure the "folders" directory exists
    base_folder_path = os.path.join(os.getcwd(), "folders")  # Get the path of the "folders" directory
    os.makedirs(base_folder_path, exist_ok=True)  # Create the "folders" directory if it doesn't exist

    # Get folder name from user input
    folder_name = input(Fore.CYAN + "Enter the folder name for the YouTube channel videos: " + Style.RESET_ALL)

    # Get channel URL from user input
    channel_url = input(Fore.CYAN + "Enter the URL of the YouTube channel (videos tab link): " + Style.RESET_ALL)

    # Get channel title
    channel = Channel(channel_url)  # Create a Channel object with the given URL
    channel_title = folder_name  # Use the user-provided folder name as the channel title

    # Create directory with channel title inside the "folders" directory
    folder_path = os.path.join(base_folder_path, channel_title)  # Get the path of the folder for this channel
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    # Print starting message
    print(Fore.GREEN + f"Downloading videos from channel '{channel_title}' to '{folder_path}'" + Style.RESET_ALL)

    # Create logs directory if it doesn't exist
    logs_directory = os.path.join(os.getcwd(), "logs", channel_title)  # Get the path of the log subdirectory for this channel
    if os.path.exists(logs_directory):
        shutil.rmtree(logs_directory)  # Remove existing log subdirectory if it exists
    os.makedirs(logs_directory, exist_ok=True)  # Create the log subdirectory

    # Log file path
    log_file_path = os.path.join(logs_directory, f"{channel_title}_failed_downloads.txt")

    # Open log file to write at the beginning
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Failed Downloads:\n\n")

    # Initialize list to store log of failed downloads
    failed_downloads = []

    # Iterate through each video in the channel
    for i, video in enumerate(channel.videos):
        # Get the file name and path for the video
        file_name = f"{video.title}.mp4"
        file_path = os.path.join(folder_path, file_name)

        # Skip download if file already exists
        if os.path.exists(file_path):
            print(Fore.YELLOW + f"Skipping file {i+1}/{len(channel)}: {video.title}. File already exists." + Style.RESET_ALL)
            continue

        try:
            # Print download status
            print(Fore.YELLOW + f"Downloading file {i+1}/{len(channel)}: {video.title}" + Style.RESET_ALL)

            # Get the highest resolution stream available with both video and audio
            stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            # Download the stream
            if stream:
                stream.download(output_path=folder_path, filename=file_name)  # Download the stream to the specified folder
                # Print file download status
                print(Fore.GREEN + f"Downloaded file {i+1}/{len(channel)}: {video.title}" + Style.RESET_ALL)
            else:
                error_message = f"No available streams for {video.title}"
                print(Fore.RED + f"Skipping file {i+1}/{len(channel)}: {video.title}. {error_message}" + Style.RESET_ALL)
                # Log failed download
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"S.No: {len(failed_downloads) + 1}\nIndex: {i+1}\nTitle: {video.title}\nError: {error_message}\n\n")
                # Log failed download to list
                failed_downloads.append((i+1, video.title, error_message))
        except AgeRestrictedError as e:
            # Handle age-restricted video specifically
            error_message = f"{video.video_id} is age restricted, and can't be accessed without logging in."
            print(Fore.RED + f"Skipping file {i+1}/{len(channel)}: {video.title}. {error_message}" + Style.RESET_ALL)
            # Log failed download
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"S.No: {len(failed_downloads) + 1}\nIndex: {i+1}\nTitle: {video.title}\nError: {error_message}\n\n")
            # Log failed download to list
            failed_downloads.append((i+1, video.title, error_message))
        except Exception as e:
            # Print error message if download fails
            error_message = str(e)
            print(Fore.RED + f"Skipping file {i+1}/{len(channel)}: {video.title}. Error: {error_message}" + Style.RESET_ALL)
            # Log failed download
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"S.No: {len(failed_downloads) + 1}\nIndex: {i+1}\nTitle: {video.title}\nError: {error_message}\n\n")
            # Log failed download to list
            failed_downloads.append((i+1, video.title, error_message))

    # Get folder size
    folder_size = get_folder_size(folder_path)  # Get the size of the downloaded folder

    # Print folder size
    print(Fore.CYAN + f"Folder size: {folder_size / (1024 * 1024)} MB" + Style.RESET_ALL)

    # Print completion message
    print(Fore.GREEN + f"All available files downloaded for channel '{channel_title}'" + Style.RESET_ALL)

    # Log failed downloads to console
    if failed_downloads:
        print(Fore.YELLOW + "Failed downloads:" + Style.RESET_ALL)
        for index, title, error in failed_downloads:
            print(Fore.RED + f"S.No: {failed_downloads.index((index, title, error)) + 1}. Index: {index}. Title: {title}. Error: {error}" + Style.RESET_ALL)

# Call the function to download the channel videos
download_channel_videos()
