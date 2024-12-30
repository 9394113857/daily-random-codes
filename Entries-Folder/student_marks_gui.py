import tkinter as tk  # Import Tkinter for GUI creation
from tkinter import messagebox  # Import messagebox for displaying pop-up messages
import csv  # Import csv module to handle reading and writing CSV files
import os  # Import os module to check if the file exists
import time  # Import time for waiting before retrying file access

# Define the CSV file name where student data will be stored
file_name = 'student_marks_data.csv'

# Function to check if the CSV file exists, if not, create it with headers
def check_file():
    if not os.path.isfile(file_name):  # Check if the file does not exist
        # Create the file with headers (including Total, Average, Grade columns)
        try:
            with open(file_name, mode='w', newline='') as file:  # Open the file in write mode
                writer = csv.writer(file)  # Create a CSV writer object
                writer.writerow(['S.No', 'Student Name', 'Telugu', 'Hindi', 'English', 'Maths', 'Science', 'Social', 'Total', 'Average', 'Grade'])  # Write headers to the file
        except Exception as e:  # If an error occurs, show an error message
            messagebox.showerror("Error", f"Failed to create CSV file: {str(e)}")
            root.quit()  # Exit the program if the file can't be created

# Function to handle file opening with error handling for file lock
def open_file_safe(mode='r'):
    retry_count = 3  # Retry 3 times before showing an error
    for attempt in range(retry_count):  # Loop through attempts
        try:
            file = open(file_name, mode, newline='')  # Try to open the file
            return file  # Return the file object if opened successfully
        except IOError:  # If there is an error in opening the file (e.g., file is locked)
            if attempt < retry_count - 1:  # If it's not the last retry attempt
                time.sleep(1)  # Wait 1 second before retrying
            else:
                messagebox.showerror("File Access Error", f"Failed to access the file after {retry_count} attempts. Please ensure the file is not open in another program.")
                root.quit()  # Exit the program if the file can't be accessed
    return None  # Return None if all retry attempts fail

# Function to add student data to the CSV file
def add_data():
    # Get the input from the GUI entry fields
    student_name = entry_name.get()  # Student name
    telugu_marks = entry_telugu.get()  # Telugu marks
    hindi_marks = entry_hindi.get()  # Hindi marks
    english_marks = entry_english.get()  # English marks
    maths_marks = entry_maths.get()  # Maths marks
    science_marks = entry_science.get()  # Science marks
    social_marks = entry_social.get()  # Social marks
    
    try:
        # Convert the marks to integers
        telugu_marks = int(telugu_marks)
        hindi_marks = int(hindi_marks)
        english_marks = int(english_marks)
        maths_marks = int(maths_marks)
        science_marks = int(science_marks)
        social_marks = int(social_marks)
    except ValueError:  # If input cannot be converted to integers (invalid input)
        messagebox.showerror("Invalid Input", "Please enter valid numbers for marks.")
        return  # Exit the function if input is invalid

    # Calculate the total marks and average
    total = telugu_marks + hindi_marks + english_marks + maths_marks + science_marks + social_marks
    average = total / 6  # Average for 6 subjects
    
    # Assign grades based on the average
    if average >= 85:
        grade = 'A'  # Grade A for average >= 85
    elif average >= 70:
        grade = 'B'  # Grade B for average >= 70
    elif average >= 50:
        grade = 'C'  # Grade C for average >= 50
    else:
        grade = 'D'  # Grade D for average < 50
    
    # Get the last serial number (S.No) from the CSV file
    try:
        file = open_file_safe('r')  # Open the file in read mode
        reader = csv.reader(file)  # Create a CSV reader object
        rows = list(reader)  # Read all rows in the CSV file
        last_row = rows[-1] if len(rows) > 1 else None  # Get the last row if available
        if last_row:
            serial_number = int(last_row[0]) + 1  # Increment serial number
        else:
            serial_number = 1  # If the file is empty, start with serial number 1
        file.close()  # Close the file after reading
    except Exception as e:  # If an error occurs, set serial number to 1
        serial_number = 1
        messagebox.showerror("Error", f"Error retrieving S.No: {str(e)}")

    # Open the CSV file and append the new student data
    try:
        file = open_file_safe('a')  # Open the file in append mode
        writer = csv.writer(file)  # Create a CSV writer object
        writer.writerow([serial_number, student_name, telugu_marks, hindi_marks, english_marks, maths_marks, science_marks, social_marks, total, average, grade])  # Write student data to the file
        file.close()  # Close the file after writing

        # Show success message
        messagebox.showinfo("Success", f"Data for {student_name} added successfully!")

        # Reset the form fields after submission
        reset_form()
    except Exception as e:  # If an error occurs during file writing
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")

# Function to reset the form fields after submitting data
def reset_form():
    entry_name.delete(0, tk.END)  # Clear the student name field
    entry_telugu.delete(0, tk.END)  # Clear the Telugu marks field
    entry_hindi.delete(0, tk.END)  # Clear the Hindi marks field
    entry_english.delete(0, tk.END)  # Clear the English marks field
    entry_maths.delete(0, tk.END)  # Clear the Maths marks field
    entry_science.delete(0, tk.END)  # Clear the Science marks field
    entry_social.delete(0, tk.END)  # Clear the Social marks field

# Function to generate the second sheet (view with calculated Total, Average, and Grade)
def generate_second_sheet():
    try:
        file = open_file_safe('r')  # Open the file in read mode
        reader = csv.reader(file)  # Create a CSV reader object
        rows = list(reader)  # Read all rows in the CSV file
        file.close()  # Close the file after reading

        # Clear any previous data in the second sheet display
        for widget in second_sheet_frame.winfo_children():
            widget.destroy()

        # Define column headers for the second sheet
        headers = ['S.No', 'Student Name', 'Telugu', 'Hindi', 'English', 'Maths', 'Science', 'Social', 'Total', 'Average', 'Grade']
        
        # Display headers in the second sheet frame
        for col, header in enumerate(headers):
            label = tk.Label(second_sheet_frame, text=header, width=12, borderwidth=2, relief="solid")  # Create label for each header
            label.grid(row=0, column=col, padx=5, pady=5)
        
        # Display student data with S.No, Total, Average, and Grade
        for row_num, row in enumerate(rows[1:], start=1):  # Start from row 1 (skipping the header)
            for col_num, value in enumerate(row):  # Loop through each column value in the row
                label = tk.Label(second_sheet_frame, text=value, width=12, borderwidth=2, relief="solid")  # Create label for each value
                label.grid(row=row_num, column=col_num, padx=5, pady=5)

    except Exception as e:  # If an error occurs while generating the second sheet
        messagebox.showerror("Error", "Failed to generate second sheet.")

# Create the main window for the Tkinter GUI
root = tk.Tk()
root.title("Student Marks Entry Form")  # Set window title

# Call check_file function to ensure CSV file exists
check_file()

# Create labels and entry fields for the student form
label_name = tk.Label(root, text="Student Name:")  
label_name.grid(row=0, column=0, padx=10, pady=5)  # Position label

entry_name = tk.Entry(root, width=30)  
entry_name.grid(row=0, column=1, padx=10, pady=5)  

# Create fields for the subjects
label_telugu = tk.Label(root, text="Telugu Marks:")  
label_telugu.grid(row=1, column=0, padx=10, pady=5)

entry_telugu = tk.Entry(root, width=30)  
entry_telugu.grid(row=1, column=1, padx=10, pady=5)

label_hindi = tk.Label(root, text="Hindi Marks:")  
label_hindi.grid(row=2, column=0, padx=10, pady=5)

entry_hindi = tk.Entry(root, width=30)  
entry_hindi.grid(row=2, column=1, padx=10, pady=5)

label_english = tk.Label(root, text="English Marks:")  
label_english.grid(row=3, column=0, padx=10, pady=5)

entry_english = tk.Entry(root, width=30)  
entry_english.grid(row=3, column=1, padx=10, pady=5)

label_maths = tk.Label(root, text="Maths Marks:")  
label_maths.grid(row=4, column=0, padx=10, pady=5)

entry_maths = tk.Entry(root, width=30)  
entry_maths.grid(row=4, column=1, padx=10, pady=5)

label_science = tk.Label(root, text="Science Marks:")  
label_science.grid(row=5, column=0, padx=10, pady=5)

entry_science = tk.Entry(root, width=30)  
entry_science.grid(row=5, column=1, padx=10, pady=5)

label_social = tk.Label(root, text="Social Marks:")  
label_social.grid(row=6, column=0, padx=10, pady=5)

entry_social = tk.Entry(root, width=30)  
entry_social.grid(row=6, column=1, padx=10, pady=5)

# Create submit and exit buttons
button_submit = tk.Button(root, text="Submit", width=15, command=add_data)  
button_submit.grid(row=7, column=0, padx=10, pady=5)

# Create exit button (replaces reset button)
button_exit = tk.Button(root, text="Exit", width=15, command=root.quit)  
button_exit.grid(row=7, column=1, padx=10, pady=5)

# Create the second sheet frame to display the student data (S.No, Total, Average, Grade)
second_sheet_frame = tk.Frame(root)
second_sheet_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Create button to generate second sheet
button_generate_sheet = tk.Button(root, text="Generate Second Sheet", width=30, command=generate_second_sheet)
button_generate_sheet.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

# Run the Tkinter event loop
root.mainloop()  # Start the GUI event loop
