import tkinter as tk
from tkinter import messagebox
import csv
import os
import time
from datetime import datetime

# Define the CSV file name where stock data will be stored
file_name = 'uptrend_charges.csv'

# Function to check if the CSV file exists, if not, create it with headers
def check_file():
    if not os.path.isfile(file_name):  # Check if the file does not exist
        # Create the file with headers
        try:
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)  # Create a CSV writer object
                writer.writerow(['S.No', 'Stock Name', 'Entry Price', 'Exit Price', 'Capital', 'Shares Bought', 
                                 'Profit per Share', 'Gross Profit', 'Net Profit', 'Date', 'Entry Time', 'Exit Time', 'Time Taken'])
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

# Function to add trade data to the CSV file
def add_data():
    stock_name = entry_stock_name.get()  # Stock Name
    entry_price = entry_entry_price.get()  # Entry Price
    exit_price = entry_exit_price.get()  # Exit Price
    capital = entry_capital.get()  # Capital
    entry_time = entry_entry_time.get()  # Entry Time
    exit_time = entry_exit_time.get()  # Exit Time
    time_taken = entry_time_taken.get()  # Time Taken (user input)
    
    try:
        # Convert the input values to the correct types
        entry_price = float(entry_price)
        exit_price = float(exit_price)
        capital = float(capital)
        
        # Calculate values based on user input
        each_share_cost = 0.20 * entry_price  # Calculate the cost of each share
        shares_bought = capital / each_share_cost  # Calculate how many shares can be bought
        profit_per_share = exit_price - entry_price  # Calculate the profit per share
        gross_profit = profit_per_share * shares_bought  # Gross profit calculation
        total_charges = 27  # Static charges
        net_profit = gross_profit - total_charges  # Net profit after deducting charges
        
        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")  # Current Date in YYYY-MM-DD format
        
        # Get the last serial number (S.No) from the CSV file
        try:
            file = open_file_safe('r')  # Open the file in read mode
            reader = csv.reader(file)
            rows = list(reader)
            last_row = rows[-1] if len(rows) > 1 else None
            serial_number = int(last_row[0]) + 1 if last_row else 1
            file.close()
        except Exception as e:
            serial_number = 1
            messagebox.showerror("Error", f"Error retrieving S.No: {str(e)}")
        
        # Write the data to the CSV file as strings (this avoids the leading zero error)
        try:
            file = open_file_safe('a')  # Open the file in append mode
            writer = csv.writer(file)
            writer.writerow([serial_number, stock_name, str(entry_price), str(exit_price), str(capital), 
                             str(shares_bought), str(profit_per_share), str(gross_profit), str(net_profit), 
                             str(current_date), str(entry_time), str(exit_time), str(time_taken)])  # Ensure all data is written as strings
            file.close()
            messagebox.showinfo("Success", f"Trade data for {stock_name} added successfully!")
            reset_form()  # Reset form after submitting the data
            display_data()  # Immediately refresh and display the updated data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for Entry Price, Exit Price, and Capital.")

# Function to reset the form after data submission
def reset_form():
    entry_stock_name.delete(0, tk.END)  # Clear stock name field
    entry_entry_price.delete(0, tk.END)  # Clear entry price field
    entry_exit_price.delete(0, tk.END)  # Clear exit price field
    entry_capital.delete(0, tk.END)  # Clear capital field
    entry_entry_time.delete(0, tk.END)  # Clear entry time field
    entry_exit_time.delete(0, tk.END)  # Clear exit time field
    entry_time_taken.delete(0, tk.END)  # Clear time taken field

# Function to display previously entered data in the second sheet
def display_data():
    try:
        file = open_file_safe('r')
        reader = csv.reader(file)
        rows = list(reader)
        file.close()
        
        for widget in second_sheet_frame.winfo_children():
            widget.destroy()  # Remove previous data display

        headers = ['S.No', 'Stock Name', 'Entry Price', 'Exit Price', 'Capital', 'Shares Bought',
                   'Profit per Share', 'Gross Profit', 'Net Profit', 'Date', 'Entry Time', 'Exit Time', 'Time Taken']
        
        for col, header in enumerate(headers):
            label = tk.Label(second_sheet_frame, text=header, width=12, borderwidth=2, relief="solid")
            label.grid(row=0, column=col, padx=5, pady=5)

        for row_num, row in enumerate(rows[1:], start=1):
            for col_num, value in enumerate(row):
                label = tk.Label(second_sheet_frame, text=value, width=12, borderwidth=2, relief="solid")
                label.grid(row=row_num, column=col_num, padx=5, pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display data: {str(e)}")

# Create the main window for the Tkinter GUI
root = tk.Tk()
root.title("Stock Trade Data Entry")

# Check if the file exists or create it if not
check_file()

# Create labels and entry fields for user input
label_stock_name = tk.Label(root, text="Stock Name:")
label_stock_name.grid(row=0, column=0, padx=10, pady=5)
entry_stock_name = tk.Entry(root, width=30)
entry_stock_name.grid(row=0, column=1, padx=10, pady=5)

label_entry_price = tk.Label(root, text="Entry Price:")
label_entry_price.grid(row=1, column=0, padx=10, pady=5)
entry_entry_price = tk.Entry(root, width=30)
entry_entry_price.grid(row=1, column=1, padx=10, pady=5)

label_exit_price = tk.Label(root, text="Exit Price:")
label_exit_price.grid(row=2, column=0, padx=10, pady=5)
entry_exit_price = tk.Entry(root, width=30)
entry_exit_price.grid(row=2, column=1, padx=10, pady=5)

label_capital = tk.Label(root, text="Capital:")
label_capital.grid(row=3, column=0, padx=10, pady=5)
entry_capital = tk.Entry(root, width=30)
entry_capital.grid(row=3, column=1, padx=10, pady=5)

label_entry_time = tk.Label(root, text="Entry Time (HH:MM):")
label_entry_time.grid(row=4, column=0, padx=10, pady=5)
entry_entry_time = tk.Entry(root, width=30)
entry_entry_time.grid(row=4, column=1, padx=10, pady=5)

label_exit_time = tk.Label(root, text="Exit Time (HH:MM):")
label_exit_time.grid(row=5, column=0, padx=10, pady=5)
entry_exit_time = tk.Entry(root, width=30)
entry_exit_time.grid(row=5, column=1, padx=10, pady=5)

label_time_taken = tk.Label(root, text="Time Taken:")
label_time_taken.grid(row=6, column=0, padx=10, pady=5)
entry_time_taken = tk.Entry(root, width=30)
entry_time_taken.grid(row=6, column=1, padx=10, pady=5)

# Button to add the data
button_add_data = tk.Button(root, text="Add Data", command=add_data)
button_add_data.grid(row=7, column=0, columnspan=2, pady=10)

# Frame for displaying the second sheet (CSV data)
second_sheet_frame = tk.Frame(root)
second_sheet_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Display data on the second sheet (CSV data) immediately
display_data()

# Run the Tkinter main loop
root.mainloop()
