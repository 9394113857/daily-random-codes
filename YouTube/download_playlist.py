from pytube import Playlist, YouTube
import os
import shutil
from colorama import init, Fore, Style
from pytube.exceptions import AgeRestrictedError
import time

# Initialize colorama to support colored terminal output
init()

# Function to get folder size
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Function to log errors to a file
def log_error(log_file_path, video_title, error_message):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"Title: {video_title}\nError: {error_message}\n\n")

# Function to download a video with retries and detailed error handling
def download_video(video, file_path, log_file_path, retries=3, delay=5):
    for attempt in range(retries):
        try:
            print(Fore.YELLOW + f"Attempt {attempt + 1}/{retries} for {video.title}" + Style.RESET_ALL)
            stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if stream:
                stream.download(output_path=os.path.dirname(file_path), filename=os.path.basename(file_path))
                print(Fore.GREEN + f"Downloaded file: {video.title}" + Style.RESET_ALL)
                return True
            else:
                raise ValueError("No available streams")
        except (ValueError, AgeRestrictedError) as e:
            error_message = f"Attempt {attempt + 1} failed for {video.title}. Error: {str(e)}"
            print(Fore.RED + error_message + Style.RESET_ALL)
            log_error(log_file_path, video.title, error_message)
            if attempt < retries - 1:
                print(Fore.YELLOW + f"Retrying in {delay} seconds..." + Style.RESET_ALL)
                time.sleep(delay)
            else:
                return False
        except Exception as e:
            error_message = f"Attempt {attempt + 1} failed for {video.title}. Error: {str(e)}"
            print(Fore.RED + error_message + Style.RESET_ALL)
            log_error(log_file_path, video.title, error_message)
            if attempt < retries - 1:
                print(Fore.YELLOW + f"Retrying in {delay} seconds..." + Style.RESET_ALL)
                time.sleep(delay)
            else:
                return False

# Function to download playlist and organize into folder
def download_playlist():
    base_folder_path = os.path.join(os.getcwd(), "folders")
    os.makedirs(base_folder_path, exist_ok=True)

    playlist_url = input(Fore.CYAN + "Enter the URL of the YouTube playlist: " + Style.RESET_ALL)

    playlist = Playlist(playlist_url)
    playlist_title = playlist.title

    folder_path = os.path.join(base_folder_path, playlist_title)
    os.makedirs(folder_path, exist_ok=True)

    print(Fore.GREEN + f"Downloading playlist '{playlist_title}' to '{folder_path}'" + Style.RESET_ALL)

    logs_directory = os.path.join(os.getcwd(), "logs", playlist_title)
    if os.path.exists(logs_directory):
        shutil.rmtree(logs_directory)
    os.makedirs(logs_directory, exist_ok=True)

    global log_file_path
    log_file_path = os.path.join(logs_directory, f"{playlist_title}_failed_downloads.txt")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Failed Downloads:\n\n")

    failed_downloads = []

    for i, video in enumerate(playlist.videos):
        file_name = f"{video.title}.mp4"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            print(Fore.YELLOW + f"Skipping file {i+1}/{len(playlist)}: {video.title}. File already exists." + Style.RESET_ALL)
            continue

        try:
            print(Fore.YELLOW + f"Downloading file {i+1}/{len(playlist)}: {video.title}" + Style.RESET_ALL)
            if not download_video(video, file_path, log_file_path):
                error_message = f"Failed to download after multiple attempts: {video.title}"
                print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. {error_message}" + Style.RESET_ALL)
                failed_downloads.append((i+1, video.title, error_message))
        except AgeRestrictedError as e:
            error_message = f"{video.video_id} is age restricted and can't be accessed without logging in."
            print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. {error_message}" + Style.RESET_ALL)
            log_error(log_file_path, video.title, error_message)
            failed_downloads.append((i+1, video.title, error_message))
        except Exception as e:
            error_message = str(e)
            print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. Error: {error_message}" + Style.RESET_ALL)
            log_error(log_file_path, video.title, error_message)
            failed_downloads.append((i+1, video.title, error_message))

    folder_size = get_folder_size(folder_path)
    print(Fore.CYAN + f"Folder size: {folder_size / (1024 * 1024):.2f} MB" + Style.RESET_ALL)
    print(Fore.GREEN + f"All available files downloaded for '{playlist_title}'" + Style.RESET_ALL)

    if failed_downloads:
        print(Fore.YELLOW + "Failed downloads:" + Style.RESET_ALL)
        for index, title, error in failed_downloads:
            print(Fore.RED + f"S.No: {failed_downloads.index((index, title, error)) + 1}. Index: {index}. Title: {title}. Error: {error}" + Style.RESET_ALL)

# Call the function to download the playlist
download_playlist()
