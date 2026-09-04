import openpyxl
import pyautogui
import time
import sys


# ============================================================
# CONFIGURATION
# ============================================================

XLSX_FILE = (
    r"E:\Office-Works\daily-random-codes"
    r"\Login-Logout local\cc.xlsx"
)

GOOGLE_LOGIN_URL = "https://accounts.google.com/signin"
YOUTUBE_URL = "https://www.youtube.com"
LOGOUT_URL = "https://accounts.google.com/logout"


# ============================================================
# COUNTDOWN
# ============================================================

def countdown(seconds, message):

    print()
    print(message)

    for remaining in range(seconds, 0, -1):

        print(
            f"\r  {remaining:02d} seconds remaining...",
            end="",
            flush=True
        )

        time.sleep(1)

    print(
        "\r  Done.                         "
    )


# ============================================================
# OPEN URL IN CHROME
# ============================================================

def open_url(url, description, wait_seconds=10):

    print()
    print("=" * 70)
    print(description)
    print("=" * 70)

    print()
    print(f"URL:")
    print(url)

    countdown(
        5,
        "Opening URL in Chrome in..."
    )

    pyautogui.hotkey(
        "ctrl",
        "l"
    )

    time.sleep(1)

    pyautogui.write(
        url,
        interval=0.03
    )

    pyautogui.press(
        "enter"
    )

    print()
    print("URL submitted.")

    countdown(
        wait_seconds,
        "Waiting for page to load..."
    )


# ============================================================
# ENTER USERNAME
# ============================================================

def enter_username(username, account_number):

    print()
    print("=" * 70)
    print(
        f"USERNAME STAGE - ACCOUNT {account_number}"
    )
    print("=" * 70)

    print()
    print(
        f"Username loaded from Excel: {username}"
    )

    print()
    print(
        "Chrome should now show the Google "
        "Email / Phone field."
    )

    print(
        "Make sure Chrome is focused."
    )

    countdown(
        5,
        "Username entry will start in..."
    )

    pyautogui.write(
        username,
        interval=0.06
    )

    print()
    print(
        f"Username entered: {username}"
    )

    pyautogui.press(
        "enter"
    )

    print(
        "Username submitted."
    )

    countdown(
        20,
        "Waiting for Google after username..."
    )


# ============================================================
# MANUAL GOOGLE LOGIN CHECKPOINT
# ============================================================

def google_login_checkpoint():

    print()
    print("=" * 70)
    print("GOOGLE LOGIN CHECKPOINT")
    print("=" * 70)

    print()
    print("Now look at Chrome.")
    print()

    print("Complete the remaining Google steps manually:")
    print()
    print("1. CAPTCHA / verification, if shown.")
    print("2. Password entry.")
    print("3. Recovery/security prompts, if shown.")
    print("4. Phone/email verification, if shown.")
    print("5. Any other Google security screen.")
    print()
    print(
        "Continue until the account is completely logged in."
    )

    print()
    print("-" * 70)
    print("When login is completely successful:")
    print("  Return to this PowerShell window.")
    print("  Press ENTER.")
    print()
    print("If login failed or you want to stop:")
    print("  Type STOP and press ENTER.")
    print("-" * 70)

    choice = input(
        "\nYour choice: "
    ).strip().lower()

    if choice == "stop":
        return False

    return True


# ============================================================
# YOUTUBE STAGE
# ============================================================

def open_youtube():

    print()
    print("=" * 70)
    print("YOUTUBE STAGE")
    print("=" * 70)

    countdown(
        5,
        "Opening YouTube in..."
    )

    pyautogui.hotkey(
        "ctrl",
        "l"
    )

    time.sleep(1)

    pyautogui.write(
        YOUTUBE_URL,
        interval=0.03
    )

    pyautogui.press(
        "enter"
    )

    print()
    print(
        f"Entering: {YOUTUBE_URL}"
    )

    print(
        "YouTube URL submitted."
    )

    countdown(
        20,
        "YouTube viewing time..."
    )


# ============================================================
# LOGOUT STAGE
# ============================================================

def logout_account():

    print()
    print("=" * 70)
    print("LOGOUT STAGE")
    print("=" * 70)

    print()
    print(
        "You can use/watch the browser during the countdown."
    )

    countdown(
        20,
        "Logout will begin in..."
    )

    pyautogui.hotkey(
        "ctrl",
        "l"
    )

    time.sleep(1)

    pyautogui.write(
        LOGOUT_URL,
        interval=0.03
    )

    pyautogui.press(
        "enter"
    )

    print()
    print(
        "Logout URL submitted."
    )

    countdown(
        20,
        "Waiting for Google logout..."
    )

    print(
        "Logout step completed."
    )


# ============================================================
# PARSE ACCOUNT NUMBERS
# ============================================================

def parse_accounts(text):

    accounts = []

    for value in text.split(","):

        value = value.strip()

        if not value:
            continue

        try:
            number = int(value)
        except ValueError:
            raise ValueError(
                f"'{value}' is not a valid account number."
            )

        if number < 1:
            raise ValueError(
                "Account numbers must be 1 or greater."
            )

        if number not in accounts:
            accounts.append(number)

    if not accounts:
        raise ValueError(
            "No account numbers were entered."
        )

    return accounts


# ============================================================
# LOAD ACCOUNT
#
# HEADER:
# Row 1 = sno / username / password
#
# Account 1 -> Excel row 2
# Account 2 -> Excel row 3
# Account 6 -> Excel row 7
# ============================================================

def load_account(ws, account_number):

    excel_row = account_number + 1

    if excel_row > ws.max_row:

        return None, (
            f"Account {account_number} does not exist. "
            f"Excel row {excel_row} is outside the sheet."
        )

    sno = ws.cell(
        row=excel_row,
        column=1
    ).value

    username = ws.cell(
        row=excel_row,
        column=2
    ).value

    password = ws.cell(
        row=excel_row,
        column=3
    ).value

    # --------------------------------------------------------
    # Validate SNO
    # --------------------------------------------------------

    if sno is None:

        return None, (
            f"Excel row {excel_row}: SNO is empty."
        )

    # --------------------------------------------------------
    # Validate username
    # --------------------------------------------------------

    if (
        username is None
        or str(username).strip() == ""
    ):

        return None, (
            f"Excel row {excel_row}: username is empty."
        )

    # --------------------------------------------------------
    # Validate password exists.
    #
    # Password is deliberately NOT displayed.
    # --------------------------------------------------------

    if (
        password is None
        or str(password).strip() == ""
    ):

        return None, (
            f"Excel row {excel_row}: password is empty."
        )

    return {
        "account": account_number,
        "excel_row": excel_row,
        "sno": sno,
        "username": str(username).strip()
    }, None


# ============================================================
# MAIN
# ============================================================

print()
print("=" * 70)
print("GOOGLE LOGIN / LOGOUT AUTOMATION - V2")
print("=" * 70)

print()
print("Excel file:")
print(XLSX_FILE)

print()
print("Chrome must already be OPEN.")

countdown(
    5,
    "Starting program in..."
)


try:

    # ========================================================
    # LOAD EXCEL
    # ========================================================

    print()
    print("=" * 70)
    print("LOADING EXCEL")
    print("=" * 70)

    wb = openpyxl.load_workbook(
        XLSX_FILE,
        data_only=True
    )

    print()
    print("Available sheets:")

    for number, sheet_name in enumerate(
        wb.sheetnames,
        start=1
    ):

        print(
            f"{number}. {sheet_name}"
        )


    # ========================================================
    # SELECT SHEET
    # ========================================================

    while True:

        try:

            sheet_number = int(
                input(
                    "\nEnter the sheet number: "
                )
            )

            if (
                sheet_number < 1
                or sheet_number > len(wb.sheetnames)
            ):

                print(
                    "Invalid sheet number."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid sheet number."
            )


    ws = wb.worksheets[
        sheet_number - 1
    ]

    print()
    print(
        f"Selected sheet: {ws.title}"
    )


    # ========================================================
    # ASK WHETHER TO SPECIFY USERS
    # ========================================================

    while True:

        answer = input(
            "\nDo you want to specify users? "
            "(yes/no): "
        ).strip().lower()

        if answer in (
            "yes",
            "no"
        ):

            break

        print(
            "Please enter yes or no."
        )


    # ========================================================
    # NO SPECIFIC USERS
    # ========================================================

    if answer == "no":

        selected_accounts = list(
            range(
                1,
                ws.max_row
            )
        )

    else:

        while True:

            try:

                account_text = input(
                    "\nEnter account numbers "
                    "(example: 1,6,10): "
                )

                selected_accounts = parse_accounts(
                    account_text
                )

                break

            except ValueError as error:

                print(
                    f"Invalid input: {error}"
                )


    # ========================================================
    # VALIDATE ACCOUNTS BEFORE OPENING GOOGLE
    # ========================================================

    print()
    print("=" * 70)
    print("VALIDATING EXCEL DATA")
    print("=" * 70)

    valid_accounts = []

    for account_number in selected_accounts:

        account, error = load_account(
            ws,
            account_number
        )

        if error:

            print()
            print(
                f"WARNING: {error}"
            )

            continue

        print()
        print("-" * 70)

        print(
            f"Account   : {account['account']}"
        )

        print(
            f"Excel row : {account['excel_row']}"
        )

        print(
            f"SNO       : {account['sno']}"
        )

        print(
            f"Username  : {account['username']}"
        )

        print(
            "Password  : [AVAILABLE]"
        )

        print(
            "Status    : READY"
        )

        print("-" * 70)

        valid_accounts.append(
            account
        )


    # ========================================================
    # STOP IF NO VALID DATA
    # ========================================================

    if not valid_accounts:

        print()
        print(
            "No valid accounts found."
        )

        print(
            "Nothing will be processed."
        )

        sys.exit()


    # ========================================================
    # RESULTS
    # ========================================================

    results = []


    # ========================================================
    # PROCESS EACH ACCOUNT
    # ========================================================

    for index, account in enumerate(
        valid_accounts,
        start=1
    ):

        account_number = account[
            "account"
        ]

        excel_row = account[
            "excel_row"
        ]

        sno = account[
            "sno"
        ]

        username = account[
            "username"
        ]


        print()
        print()
        print("=" * 70)

        print(
            f"PROCESSING ACCOUNT {account_number}"
        )

        print(
            f"Excel row : {excel_row}"
        )

        print(
            f"SNO       : {sno}"
        )

        print(
            f"Progress  : "
            f"{index}/{len(valid_accounts)}"
        )

        print("=" * 70)


        # ====================================================
        # GOOGLE SIGN-IN
        # ====================================================

        open_url(
            GOOGLE_LOGIN_URL,
            "GOOGLE SIGN-IN",
            wait_seconds=10
        )


        # ====================================================
        # USERNAME
        # ====================================================

        enter_username(
            username,
            account_number
        )


        # ====================================================
        # MANUAL PASSWORD / SECURITY CHECKPOINT
        # ====================================================

        login_success = (
            google_login_checkpoint()
        )


        # ====================================================
        # STOP REQUESTED
        # ====================================================

        if not login_success:

            results.append({
                "account": account_number,
                "sno": sno,
                "status": "STOPPED"
            })

            print()
            print(
                "Stopping entire automation."
            )

            break


        # ====================================================
        # LOGIN CONFIRMED
        # ====================================================

        print()
        print(
            "Google login confirmed."
        )

        results.append({
            "account": account_number,
            "sno": sno,
            "status": "LOGIN OK"
        })


        # ====================================================
        # YOUTUBE
        # ====================================================

        open_youtube()


        # ====================================================
        # LOGOUT
        # ====================================================

        logout_account()


        # ====================================================
        # MARK COMPLETED
        # ====================================================

        results[-1][
            "status"
        ] = "COMPLETED"


        print()
        print(
            f"Account {account_number} completed."
        )


        # ====================================================
        # WAIT BEFORE NEXT ACCOUNT
        # ====================================================

        if index < len(valid_accounts):

            countdown(
                10,
                "Preparing next selected account..."
            )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    print()
    print()
    print("=" * 70)
    print("FINAL REPORT")
    print("=" * 70)

    print()

    print(
        f"Selected sheet : {ws.title}"
    )

    print(
        f"Requested      : "
        f"{len(selected_accounts)}"
    )

    print(
        f"Valid accounts : "
        f"{len(valid_accounts)}"
    )

    print(
        f"Processed      : "
        f"{len(results)}"
    )

    print()

    print(
        "+----------+----------+------------------+"
    )

    print(
        "| Account  | SNO      | Status           |"
    )

    print(
        "+----------+----------+------------------+"
    )

    for result in results:

        print(
            f"| "
            f"{str(result['account']):<8} "
            f"| "
            f"{str(result['sno']):<8} "
            f"| "
            f"{result['status']:<16} "
            f"|"
        )

    print(
        "+----------+----------+------------------+"
    )

    print()
    print(
        "Passwords are not displayed by the program."
    )

    print()
    print("=" * 70)
    print("AUTOMATION FINISHED")
    print("=" * 70)


except KeyboardInterrupt:

    print()
    print("=" * 70)
    print("PROGRAM INTERRUPTED")
    print("=" * 70)


except Exception as error:

    print()
    print("=" * 70)
    print("PROGRAM ERROR")
    print("=" * 70)

    print(
        f"{type(error).__name__}: {error}"
    )

    print("=" * 70)
