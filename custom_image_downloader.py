import os
import requests
from bs4 import BeautifulSoup
import zipfile

# Function to scrape the number of pages from the provided URL
def get_total_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_links = soup.find('div', class_='pagination').find_all('a')
    return len(page_links)

# Function to download images from a page and save them in a folder
def download_images_from_page(page_url, page_number):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    image_tags = soup.find_all('img', class_='bbcode_img')
    page_folder = str(page_number)
    os.makedirs(page_folder, exist_ok=True)
    for i, img_tag in enumerate(image_tags, 1):
        img_url = img_tag['src']
        img_data = requests.get(img_url).content
        with open(os.path.join(page_folder, f'{i}.jpg'), 'wb') as f:
            f.write(img_data)

# Main function
def main():
    base_url = input("Enter the base URL of the page (excluding the page number): ")
    total_pages = get_total_pages(base_url + '1')
    print(f"Detected {total_pages} pages.")

    # Download images from each page
    for page_num in range(1, total_pages + 1):
        page_url = base_url + str(page_num)
        download_images_from_page(page_url, page_num)

    # Zip the folders
    with zipfile.ZipFile('site_images.zip', 'w') as zip_file:
        for folder_name in os.listdir('.'):
            if os.path.isdir(folder_name):
                for dirpath, _, filenames in os.walk(folder_name):
                    for filename in filenames:
                        zip_file.write(os.path.join(dirpath, filename), arcname=os.path.join(folder_name, filename))

    print("Images downloaded and zipped successfully.")

if __name__ == "__main__":
    main()
