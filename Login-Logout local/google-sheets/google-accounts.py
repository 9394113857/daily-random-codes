import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyautogui

# Function to perform login actions
def login(username, password):
    pyautogui.write(username)
    pyautogui.press('enter')
    print(f"2. Typing Username: {username}")
    pyautogui.sleep(5)

    pyautogui.write(password)
    pyautogui.press('enter')
    print("3. Typing Password")
    pyautogui.sleep(5)

    pyautogui.press('f6')

    YouTube = "www.youtube.com"
    pyautogui.write(YouTube)
    pyautogui.press('enter')
    print("4. Entering into YouTube")
    pyautogui.sleep(5)

def logout():
    pyautogui.press('f6')
    logout_url = "https://accounts.google.com/logout"
    pyautogui.write(logout_url)
    pyautogui.press('enter')
    print("5. Logged out successfully")
    pyautogui.sleep(5)

pyautogui.sleep(5)

# Authenticate with Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = 'D:\\daily-random-codes-main\\Login-Logout local\\google-sheets\\heroic-charter-421611-53f3dd0426e9.json'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1xKH-0Ju9Z3c8MabnWoWMYD3uJRUNBGO8/edit?usp=sharing'

def authenticate_and_get_data(credentials_path, spreadsheet_url, scope):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(spreadsheet_url)
    worksheet = sheet.get_worksheet(0)
    return worksheet.get_all_values()

try:
    data = authenticate_and_get_data(credentials_path, spreadsheet_url, scope)
except Exception as e:
    print("Error during authentication or fetching data:", e)
    print("Please ensure the service account has access to the Google Sheet.")
    raise

header = data[0]
data = data[1:]

sno_index = header.index('Sno')
username_index = header.index('UserName')
password_index = header.index('Password')

for i, row in enumerate(data, start=1):
    sno = row[sno_index]
    username = row[username_index]
    password = row[password_index]
    
    print(f"\nExecuting tasks for Row {i} (SNO: {sno})")
    login(username, password)
    logout()
    pyautogui.sleep(5)

print("\nAll tasks completed for all users.")
