import pandas as pd
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

# Function to perform logout actions
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

# Load data from the Excel file
excel_file_name = "c.xlsx"
sheet_name = "Recently Created Accounts"
df = pd.read_excel(excel_file_name, sheet_name=sheet_name)

rows_to_process = input("Do you want to specify rows to process? (yes/no): ")
if rows_to_process.lower() == "yes":
    row_numbers = input("Enter the row numbers separated by commas (e.g., 1,2,3): ")
    rows = [int(row.strip()) for row in row_numbers.split(",")]
else:
    rows = None

# Add sleep time after taking row numbers input
pyautogui.sleep(5)

# Loop through each row in the DataFrame
for i, row in df.iterrows():
    sno = row['sno']
    username = row['username']
    password = row['password']

    # Check if the row needs to be processed based on user input
    if rows is None or (i + 1) in rows:
        print(f"\nExecuting tasks for User {i + 1} (SNO: {sno})")
        login(username, password)  # Perform login actions
        logout()  # Perform logout actions

        # Wait for some time before moving to the next user (adjust sleep time as needed)
        pyautogui.sleep(5)

print("\nAll tasks completed for all users.")
