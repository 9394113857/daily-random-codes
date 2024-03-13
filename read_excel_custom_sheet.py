import openpyxl

def read_excel_file(file_path, sheet_name):
    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)
    
    # Select the worksheet by name
    worksheet = workbook[sheet_name]
    
    # Get the headers from the first row
    headers = [cell.value for cell in worksheet[1]]
    
    # Initialize an empty list to store row-wise data
    data = []
    
    # Iterate over rows starting from the second row
    for row in worksheet.iter_rows(min_row=2, values_only=True):
        # Create a dictionary with headers as keys and row values as values
        row_data = dict(zip(headers, row))
        # Append the dictionary to the data list
        data.append(row_data)
    
    # Close the workbook
    workbook.close()
    
    return data

# Example usage
file_path = "example.xlsx"  # Change this to your file path
sheet_name = "Sheet1"       # Change this to your sheet name
data = read_excel_file(file_path, sheet_name)
print(data)
