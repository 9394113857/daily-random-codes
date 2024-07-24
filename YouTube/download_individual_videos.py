from pytube import YouTube
import os
import time
from colorama import init, Fore, Style
from pytube.exceptions import AgeRestrictedError

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
def download_video(video_url, folder_path, log_file_path, retries=3, delay=5):
    for attempt in range(retries):
        try:
            video = YouTube(video_url)
            print(Fore.YELLOW + f"Attempt {attempt + 1}/{retries} for {video.title}" + Style.RESET_ALL)
            stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if stream:
                file_path = os.path.join(folder_path, f"{video.title}.mp4")
                if os.path.exists(file_path):
                    print(Fore.YELLOW + f"File already exists: {file_path}" + Style.RESET_ALL)
                    return True
                stream.download(output_path=folder_path, filename=f"{video.title}.mp4")
                print(Fore.GREEN + f"Downloaded file: {file_path}" + Style.RESET_ALL)
                return True
            else:
                raise ValueError("No available streams")
        except (ValueError, AgeRestrictedError) as e:
            error_message = f"Attempt {attempt + 1} failed for {video_url}. Error: {str(e)}"
            print(Fore.RED + error_message + Style.RESET_ALL)
            log_error(log_file_path, video_url, error_message)
            if attempt < retries - 1:
                print(Fore.YELLOW + f"Retrying in {delay} seconds..." + Style.RESET_ALL)
                time.sleep(delay)
            else:
                return False
        except Exception as e:
            error_message = f"Attempt {attempt + 1} failed for {video_url}. Error: {str(e)}"
            print(Fore.RED + error_message + Style.RESET_ALL)
            log_error(log_file_path, video_url, error_message)
            if attempt < retries - 1:
                print(Fore.YELLOW + f"Retrying in {delay} seconds..." + Style.RESET_ALL)
                time.sleep(delay)
            else:
                return False

# Function to download individual videos
def download_individual_videos():
    base_folder_path = os.path.join(os.getcwd(), "folders")
    os.makedirs(base_folder_path, exist_ok=True)
    
    total_attempts = 0
    successful_downloads = 0
    failed_downloads = []

    while True:
        video_url = input(Fore.CYAN + "Enter the YouTube video URL: " + Style.RESET_ALL)
        folder_name = input(Fore.CYAN + "Enter the folder name for this video: " + Style.RESET_ALL)

        folder_path = os.path.join(base_folder_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        log_file_path = os.path.join(folder_path, 'failed_downloads.txt')

        if download_video(video_url, folder_path, log_file_path):
            successful_downloads += 1
        else:
            failed_downloads.append(video_url)
        
        total_attempts += 1

        cont = input(Fore.CYAN + "Do you want to download another video? (yes/exit): " + Style.RESET_ALL).strip().lower()
        if cont == 'exit':
            break

    print(Fore.GREEN + f"Download session ended. Total attempts: {total_attempts}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Successful downloads: {successful_downloads}" + Style.RESET_ALL)
    if failed_downloads:
        print(Fore.RED + "Failed downloads:" + Style.RESET_ALL)
        for url in failed_downloads:
            print(Fore.RED + f"URL: {url}" + Style.RESET_ALL)
    print(Fore.GREEN + "You have exited the download session." + Style.RESET_ALL)

# Call the function to start downloading individual videos
download_individual_videos()
