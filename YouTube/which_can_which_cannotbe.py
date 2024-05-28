from pytube import Playlist
from pytube.exceptions import AgeRestrictedError
from colorama import init, Fore, Style
import time

# Initialize colorama to support colored terminal output
init()

# Function to check and categorize videos
def categorize_videos(playlist_url):
    try:
        # Get playlist title and videos
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title
        videos = playlist.videos
        total_videos = len(videos)

        # Print starting message
        print(Fore.GREEN + f"Checking videos in playlist '{playlist_title}'" + Style.RESET_ALL)
        print(Fore.CYAN + f"Total videos in the playlist: {total_videos}\n" + Style.RESET_ALL)

        # Initialize lists to store video statuses
        can_be_downloaded = []
        cannot_be_downloaded = []

        # Print table headers
        print("\n" + Fore.CYAN + Style.BRIGHT + "Video Status:" + Style.RESET_ALL)
        print(f"{'S.No':<5} {'Title':<70} {'Status':<30}")
        print("=" * 110)

        # Iterate through each video in the playlist
        for i, video in enumerate(videos):
            try:
                # Check for available streams
                stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

                if stream:
                    can_be_downloaded.append((i + 1, video.title))  # Add to downloadable list
                    print(Fore.GREEN + f"{i + 1:<5} {video.title:<70} {'Can be downloaded':<30}" + Style.RESET_ALL)
                else:
                    cannot_be_downloaded.append((i + 1, video.title, "No available streams"))
                    print(Fore.RED + f"{i + 1:<5} {video.title:<70} {'Cannot be downloaded':<30}" + Style.RESET_ALL)
            except AgeRestrictedError:
                cannot_be_downloaded.append((i + 1, video.title, "Age restricted"))
                print(Fore.RED + f"{i + 1:<5} {video.title:<70} {'Age restricted':<30}" + Style.RESET_ALL)
            except Exception as e:
                cannot_be_downloaded.append((i + 1, video.title, str(e)))
                print(Fore.RED + f"{i + 1:<5} {video.title:<70} {'Error':<30}" + Style.RESET_ALL)

            # Adding a small delay to simulate real-time processing and scrolling effect
            time.sleep(0.5)

        # Print summary
        print("\n" + Fore.GREEN + f"Total videos that can be downloaded: {len(can_be_downloaded)}" + Style.RESET_ALL)
        print(Fore.RED + f"Total videos that cannot be downloaded: {len(cannot_be_downloaded)}" + Style.RESET_ALL)

    except KeyError:
        print(Fore.RED + "Error: The provided URL does not seem to be a valid YouTube playlist URL." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}" + Style.RESET_ALL)

# Get playlist URL from user input
try:
    playlist_url = input(Fore.CYAN + "Enter the URL of the YouTube playlist: " + Style.RESET_ALL)
    categorize_videos(playlist_url)
except Exception as e:
    print(Fore.RED + f"An error occurred while reading the input: {str(e)}" + Style.RESET_ALL)