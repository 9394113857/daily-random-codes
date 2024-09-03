import ctypes  # Import the ctypes module to interact with C functions

# ANSI escape codes for colors
class Style:
    GREEN = '\033[92m'  # Green color for successful emptying
    RED = '\033[91m'    # Red color for errors or already empty
    END = '\033[0m'     # Reset color

def clear_recycle_bin():
    # Define the SHEmptyRecycleBin function from the shell32 library
    SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW

    # Define the flags for the SHEmptyRecycleBin function
    # SHERB_NOCONFIRMATION: Do not ask for confirmation before deleting
    # SHERB_NOPROGRESSUI: Do not show a progress dialog box
    # SHERB_NOSOUND: Do not play a sound when the function is executed
    flags = 0x00000001 | 0x00000002 | 0x00000004

    # Call the SHEmptyRecycleBin function with specified flags
    result = SHEmptyRecycleBin(None, None, flags)

    # Check the result of the function call
    if result == 0:
        # If the result is 0, the Recycle Bin was successfully emptied
        print(Style.GREEN + "Recycle Bin has been emptied." + Style.END)
    elif result == 0x80070091:
        # If the result is 0x80070091, the Recycle Bin is already empty
        print(Style.RED + "The Recycle Bin is already empty." + Style.END)
    elif result == -2147418113:  # E_UNEXPECTED
        # If the result is -2147418113, an unexpected error occurred
        print(Style.RED + "Recycle Bin is already empty or an unexpected error occurred." + Style.END)
    else:
        # If the result is any other value, print the error code
        print(Style.RED + f"Failed to empty Recycle Bin. Error code: {result}" + Style.END)

if __name__ == "__main__":
    # Call the function to clear the Recycle Bin when the script is executed
    clear_recycle_bin()

"""
Comments Added:
1.	Imports: Importing the ctypes module to interact with Windows API functions.
2.	Style Class: Defining ANSI escape codes for text colors.
3.	Function Definition: clear_recycle_bin() to handle emptying the Recycle Bin.
4.	Define Function: Loading the SHEmptyRecycleBinW function from the shell32 library.
5.	Flags: Setting flags to specify no confirmation, no progress UI, and no sound.
6.	Call Function: Calling the SHEmptyRecycleBin function with the specified flags.
7.	Check Result:
o	Success: If the result is 0, the Recycle Bin was emptied successfully.
o	Already Empty: If the result is 0x80070091, the Recycle Bin was already empty.
o	Unexpected Error: If the result is -2147418113, an unexpected error occurred.
o	Other Errors: Printing the error code for other failure cases.
8.	Main Block: Executing the clear_recycle_bin() function if the script is run directly.
"""


    
