import csv
import pyautogui

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

# Read username and password from CSV file
with open(csv_file_name, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Type the username and press Enter
        pyautogui.write(row['username'])
        pyautogui.press('enter')
        print(f"2. Typing Username: {row['username']}")
        pyautogui.sleep(5)

        # Type the password and press Enter
        pyautogui.write(row['password'])
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

        # Optional: You may want to close the browser or perform other actions after logging in

        # Note: Ensure that the focus is on the correct window/browser tab before running the script

        pyautogui.write(['f6'])
        logout = "https://accounts.google.com/logout"
        pyautogui.typewrite(logout)
        pyautogui.typewrite("\n")
        print("5. Logged out successfully")