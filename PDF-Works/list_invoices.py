import os
from tabulate import tabulate

# Take directory input from user
directory = input("Enter the directory path: ")

# Check if the directory exists
if not os.path.exists(directory):
    print("Invalid directory path.")
else:
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Filter the files to include only PDFs
    pdf_files = [f for f in files if f.endswith('.pdf')]

    # Prepare data for tabular format (S.No and Invoice columns)
    table_data = [[i+1, pdf_file] for i, pdf_file in enumerate(pdf_files)]

    # Check if there are any PDF files in the directory
    if not table_data:
        print("No PDF files found in the directory.")
    else:
        # Display the table
        print(tabulate(table_data, headers=["S.No", "Invoice"], tablefmt="grid"))
