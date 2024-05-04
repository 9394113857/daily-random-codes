import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyautogui

# Function to perform login actions
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
    pyautogui.sleep(5)

    # Press 'f6' key again (optional, remove if not needed)
    pyautogui.write(['f6'])

    # Type the YouTube URL and press Enter
    YouTube = "www.youtube.com"
    pyautogui.write(YouTube)
    pyautogui.press('enter')
    print("4. Entering into YouTube")

    # Add a delay or sleep to allow time for the page to load (adjust sleep time as needed)
    pyautogui.sleep(5)  # Changed sleep time for page load

# Function to perform logout actions
def logout():
    pyautogui.write(['f6'])
    logout_url = "https://accounts.google.com/logout"
    pyautogui.write(logout_url)
    pyautogui.press('enter')
    print("5. Logged out successfully")
    pyautogui.sleep(5)  # Changed sleep time after logout

# Sleep for 5 seconds before starting to allow time to focus on the target window
pyautogui.sleep(5)  # Changed initial sleep time

# Authenticate with Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('D:\\daily-random-codes-main\\Login-Logout local\\google-sheets\\heroic-charter-421611-53f3dd0426e9.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheets document
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1xKH-0Ju9Z3c8MabnWoWMYD3uJRUNBGO8/edit?usp=sharing')

# Select the first worksheet
worksheet = sheet.get_worksheet(0)  # Assuming the data is in the first sheet

# Read sno, username, and password from Google Sheets
data = worksheet.get_all_values()[1:]  # Exclude header row

# Loop through each row in the Google Sheets document
for i, row in enumerate(data, start=1):
    sno, username, password = row
    print(f"\nExecuting tasks for Row {i} (SNO: {sno})")
    login(username, password)  # Perform login actions
    logout()  # Perform logout actions

    # Wait for some time before moving to the next row (adjust sleep time as needed)
    pyautogui.sleep(5)  # Changed sleep time after processing each row

print("\nAll tasks completed for all users.")
