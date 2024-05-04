# Import necessary libraries
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style

# Function to detect images on a webpage
def detect_images(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    # Raise an exception if the response status code is not successful
    response.raise_for_status()
    # Parse the HTML content of the response
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all image tags in the parsed HTML
    images = soup.find_all('img')
    # Print a message indicating the page being processed and the number of images detected
    print(Fore.BLUE + Style.BRIGHT + f"\nDownloading images from page {url.split('=')[-1]}:" + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + f"Detected {len(images)} images on the page." + Style.RESET_ALL)
    # Return the list of detected images
    return images

# Function to download images from multiple pages
def download_images(url, page_range, base_folder=None, overwrite=False):
    # Check if base folder name is provided
    if base_folder is None:
        print("Base folder name is required.")
        return

    # Create the base folder if it doesn't exist
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        print(f"The base folder {Fore.YELLOW + Style.BRIGHT + base_folder + Style.RESET_ALL} has been created.")
    else:
        print(f"The base folder {Fore.YELLOW + Style.BRIGHT + base_folder + Style.RESET_ALL} already exists.")

    # Track total number of images downloaded
    total_images_downloaded = 0  

    # Loop through the specified range of pages
    for page_number in range(page_range[0], page_range[1] + 1):
        # Construct the URL for the current page
        page_url = f"{url}&page={page_number}"
        # Print a message indicating the current page being processed
        print(f"\nDownloading images from page {Fore.BLUE + Style.BRIGHT + str(page_number) + Style.RESET_ALL}:")
        # Detect images on the current page
        images = detect_images(page_url)
        # Create folder for current page
        folder_name = f"{base_folder}/page_number_{page_number}"

        # Check if folder exists and contains files
        if os.path.exists(folder_name) and len(os.listdir(folder_name)) > 0:
            response = input(f"The folder {Fore.YELLOW + Style.BRIGHT + folder_name + Style.RESET_ALL} already contains files. Do you want to delete its contents? (yes/no): ").lower()
            if response == 'yes':
                # Delete all files in the folder
                for file_name in os.listdir(folder_name):
                    file_path = os.path.join(folder_name, file_name)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")
                print(f"All files in {Fore.YELLOW + Style.BRIGHT + folder_name + Style.RESET_ALL} folder have been deleted.")
            else:
                print("Skipping download. No files were deleted.")
                continue

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"The folder {Fore.YELLOW + Style.BRIGHT + folder_name + Style.RESET_ALL} has been created.")
        else:
            print(f"The folder {Fore.YELLOW + Style.BRIGHT + folder_name + Style.RESET_ALL} already exists.")

        count = 0
        # Loop through detected images
        for img in images:
            # Construct the URL for the current image
            img_url = urljoin(page_url, img['src'])
            # Check if image URL ends with '.jpg'
            if img_url.endswith('.jpg'):
                # Construct the filename for the image
                filename = os.path.join(folder_name, os.path.basename(img_url))
                # Check if overwrite flag is set or if file doesn't exist
                if overwrite or not os.path.exists(filename):
                    try:
                        # Download and save the image
                        with open(filename, 'wb') as f:
                            image_content = requests.get(img_url).content
                            f.write(image_content)
                            print(Fore.GREEN + Style.BRIGHT + f"Downloaded: {os.path.basename(img_url)}" + Style.RESET_ALL)
                            count += 1
                            total_images_downloaded += 1
                    except Exception as e:
                        print(Fore.RED + Style.BRIGHT + f"Failed to download {os.path.basename(img_url)}: {e}" + Style.RESET_ALL)

        # Print the number of images downloaded for the current page
        print(f"{Fore.RED + Style.BRIGHT}Downloaded {count} images from page {page_number} to {folder_name} folder.{Style.RESET_ALL}")

    # Print the total number of images downloaded
    print(f"\nTotal images downloaded: {Fore.GREEN + Style.BRIGHT + str(total_images_downloaded) + Style.RESET_ALL}")
    print(Fore.GREEN + Style.BRIGHT + "Download process completed." + Style.RESET_ALL)

# Example usage:
url = "https://xossipfap.net/forum/printthread.php?tid=43505&page="
base_folder = input("Enter the base folder name: ")
page_range = [int(input("Enter the start page number: ")), int(input("Enter the end page number: "))]

download_images(url, page_range, base_folder, overwrite=True)
