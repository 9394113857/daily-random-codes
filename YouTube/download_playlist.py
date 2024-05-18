from pytube import Playlist
import os
import shutil

# Function to get folder size
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Function to download playlist and organize into folder
def download_playlist():
    # Ensure the "folders" directory exists
    base_folder_path = os.path.join(os.getcwd(), "folders")
    os.makedirs(base_folder_path, exist_ok=True)

    # Get playlist URL from user input
    playlist_url = input("Enter the URL of the YouTube playlist: ")

    # Get playlist title
    playlist = Playlist(playlist_url)
    playlist_title = playlist.title

    # Create directory with playlist title inside the "folders" directory
    folder_path = os.path.join(base_folder_path, playlist_title)
    os.makedirs(folder_path, exist_ok=True)

    # Print starting message
    print(f"Downloading playlist '{playlist_title}' to '{folder_path}'")

    # Iterate through each video in the playlist
    for i, video in enumerate(playlist.videos):
        try:
            # Print download status
            print(f"Downloading file {i+1}/{len(playlist)}: {video.title}")

            # Get the highest resolution stream available with both video and audio
            stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            # Download the stream
            if stream:
                stream.download(output_path=folder_path)
                # Print file download status
                print(f"Downloaded file {i+1}/{len(playlist)}: {video.title}")
            else:
                print(f"Skipping file {i+1}/{len(playlist)}: {video.title}. No available streams.")
        except Exception as e:
            # Print error message if download fails
            print(f"Skipping file {i+1}/{len(playlist)}: {video.title}. Error: {str(e)}")

    # Get folder size
    folder_size = get_folder_size(folder_path)

    # Print folder size
    print(f"Folder size: {folder_size / (1024 * 1024)} MB")

    # Print completion message
    print(f"All available files downloaded for '{playlist_title}'")

# Call the function to download the playlist
download_playlist()
