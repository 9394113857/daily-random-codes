import ctypes

def clear_recycle_bin():
    # Define the SHEmptyRecycleBin function
    SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW

    # Define the flags for the SHEmptyRecycleBin function
    # SHERB_NOCONFIRMATION: Do not ask for confirmation before deleting
    # SHERB_NOPROGRESSUI: Do not show a progress dialog box
    # SHERB_NOSOUND: Do not play a sound when the function is executed
    flags = 0x00000001 | 0x00000002 | 0x00000004

    # Call the SHEmptyRecycleBin function
    result = SHEmptyRecycleBin(None, None, flags)

    # Check the result
    if result == 0:
        print("Recycle Bin has been emptied.")
    elif result == 0x80070091:
        print("The Recycle Bin is already empty.")
    elif result == -2147418113:  # E_UNEXPECTED
        print("Recycle Bin is already empty or unexpected error occurred.")
    else:
        print(f"Failed to empty Recycle Bin. Error code: {result}")

if __name__ == "__main__":
    clear_recycle_bin()
