# Import necessary libraries
from pytube import Playlist  # Import Playlist class from pytube module for downloading YouTube playlists
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

# Function to download playlist and organize into folder
def download_playlist():
    # Ensure the "folders" directory exists
    base_folder_path = os.path.join(os.getcwd(), "folders")  # Get the path of the "folders" directory
    os.makedirs(base_folder_path, exist_ok=True)  # Create the "folders" directory if it doesn't exist

    # Get playlist URL from user input
    playlist_url = input(Fore.CYAN + "Enter the URL of the YouTube playlist: " + Style.RESET_ALL)

    # Get playlist title
    playlist = Playlist(playlist_url)  # Create a Playlist object with the given URL
    playlist_title = playlist.title  # Get the title of the playlist

    # Create directory with playlist title inside the "folders" directory
    folder_path = os.path.join(base_folder_path, playlist_title)  # Get the path of the folder for this playlist
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    # Print starting message
    print(Fore.GREEN + f"Downloading playlist '{playlist_title}' to '{folder_path}'" + Style.RESET_ALL)

    # Create logs directory if it doesn't exist
    logs_directory = os.path.join(os.getcwd(), "logs", playlist_title)  # Get the path of the log subdirectory for this playlist
    if os.path.exists(logs_directory):
        shutil.rmtree(logs_directory)  # Remove existing log subdirectory if it exists
    os.makedirs(logs_directory, exist_ok=True)  # Create the log subdirectory

    # Log file path
    log_file_path = os.path.join(logs_directory, f"{playlist_title}_failed_downloads.txt")

    # Open log file to write at the beginning
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Failed Downloads:\n\n")

    # Initialize list to store log of failed downloads
    failed_downloads = []

    # Iterate through each video in the playlist
    for i, video in enumerate(playlist.videos):
        # Get the file name and path for the video
        file_name = f"{video.title}.mp4"
        file_path = os.path.join(folder_path, file_name)

        # Skip download if file already exists
        if os.path.exists(file_path):
            print(Fore.YELLOW + f"Skipping file {i+1}/{len(playlist)}: {video.title}. File already exists." + Style.RESET_ALL)
            continue

        try:
            # Print download status
            print(Fore.YELLOW + f"Downloading file {i+1}/{len(playlist)}: {video.title}" + Style.RESET_ALL)

            # Get the highest resolution stream available with both video and audio
            stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            # Download the stream
            if stream:
                stream.download(output_path=folder_path, filename=file_name)  # Download the stream to the specified folder
                # Print file download status
                print(Fore.GREEN + f"Downloaded file {i+1}/{len(playlist)}: {video.title}" + Style.RESET_ALL)
            else:
                error_message = f"No available streams for {video.title}"
                print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. {error_message}" + Style.RESET_ALL)
                # Log failed download
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"S.No: {len(failed_downloads) + 1}\nIndex: {i+1}\nTitle: {video.title}\nError: {error_message}\n\n")
                # Log failed download to list
                failed_downloads.append((i+1, video.title, error_message))
        except AgeRestrictedError as e:
            # Handle age-restricted video specifically
            error_message = f"{video.video_id} is age restricted, and can't be accessed without logging in."
            print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. {error_message}" + Style.RESET_ALL)
            # Log failed download
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"S.No: {len(failed_downloads) + 1}\nIndex: {i+1}\nTitle: {video.title}\nError: {error_message}\n\n")
            # Log failed download to list
            failed_downloads.append((i+1, video.title, error_message))
        except Exception as e:
            # Print error message if download fails
            error_message = str(e)
            print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. Error: {error_message}" + Style.RESET_ALL)
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
    print(Fore.GREEN + f"All available files downloaded for '{playlist_title}'" + Style.RESET_ALL)

    # Log failed downloads to console
    if failed_downloads:
        print(Fore.YELLOW + "Failed downloads:" + Style.RESET_ALL)
        for index, title, error in failed_downloads:
            print(Fore.RED + f"S.No: {failed_downloads.index((index, title, error)) + 1}. Index: {index}. Title: {title}. Error: {error}" + Style.RESET_ALL)

# Call the function to download the playlist
download_playlist()
