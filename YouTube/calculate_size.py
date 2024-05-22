from pytube import Playlist
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

# Function to get the size of a video stream
def get_stream_size(stream):
    response = stream.stream_to_buffer()
    response.seek(0, os.SEEK_END)
    return response.tell()

# Function to calculate the size of the playlist without downloading
def calculate_playlist_size():
    # Get playlist URL from user input
    playlist_url = input(Fore.CYAN + "Enter the URL of the YouTube playlist: " + Style.RESET_ALL)

    # Get playlist title
    playlist = Playlist(playlist_url)
    playlist_title = playlist.title

    # Print starting message
    print(Fore.GREEN + f"Calculating size of playlist '{playlist_title}'" + Style.RESET_ALL)

    total_size = 0

    # Iterate through each video in the playlist
    for i, video in enumerate(playlist.videos):
        try:
            # Print status message
            print(Fore.YELLOW + f"Checking file {i+1}/{len(playlist)}: {video.title}" + Style.RESET_ALL)

            # Get the highest resolution stream available with both video and audio
            stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            if stream:
                # Calculate the size of the stream
                stream_size = get_stream_size(stream)
                total_size += stream_size
                # Print file size status
                print(Fore.GREEN + f"Size of file {i+1}/{len(playlist)}: {stream_size / (1024 * 1024)} MB" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. No available streams." + Style.RESET_ALL)
        except Exception as e:
            # Print error message if size calculation fails
            print(Fore.RED + f"Skipping file {i+1}/{len(playlist)}: {video.title}. Error: {str(e)}" + Style.RESET_ALL)

    # Print total folder size
    print(Fore.CYAN + f"Total size of the playlist '{playlist_title}': {total_size / (1024 * 1024)} MB" + Style.RESET_ALL)

# Call the function to calculate the playlist size
calculate_playlist_size()
