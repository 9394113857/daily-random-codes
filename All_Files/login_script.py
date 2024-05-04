# Save this code in a file, for example, login_script.py

import csv
import pyautogui

def login(username, password):
    # Type the username and press Enter
    pyautogui.write(username)
    pyautogui.press('enter')
    print(f"2. Typing Username: {username}")
    pyautogui.sleep(5)

    # Type the password and press Enter
    pyautogui.write(password)
    pyautogui.press('enter')
    print("3. Typing Password")
    pyautogui.sleep(10)

    # Press 'f6' key again (optional, remove if not needed)
    pyautogui.write(['f6'])

    # Type the YouTube URL and press Enter
    YouTube = "www.youtube.com"
    pyautogui.write(YouTube)
    pyautogui.press('enter')
    print("4. Entering into YouTube")

    # Add a delay or sleep to allow time for the page to load (adjust sleep time as needed)
    pyautogui.sleep(10)

def logout():
    pyautogui.write(['f6'])
    logout_url = "https://accounts.google.com/logout"
    pyautogui.write(logout_url)
    pyautogui.press('enter')
    print("5. Logged out successfully")

# Sleep for 5 seconds before starting to allow time to focus on the target window
pyautogui.sleep(5)

# Press 'f6' key (optional, remove if not needed)
pyautogui.write(['f6'])

# Type the URL directly using pyautogui
link = "https://accounts.google.com/signin"
pyautogui.write(link)
pyautogui.press('enter')  # Press Enter to navigate to the URL
print("1. Typing URL")

# Wait for the login page to load (adjust sleep time as needed)
pyautogui.sleep(10)

# Hardcode the CSV file name
csv_file_name = "credentials.csv"

# Read sno, username, and password from CSV file
try:
    with open(csv_file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sno = row['sno']
            username = row['username']  # Assuming 'username' is another column in your CSV
            password = row['password']  # Assuming 'password' is another column in your CSV

            login(username, password)
            logout()
except Exception as e:
    print(f"Error: {e}")
