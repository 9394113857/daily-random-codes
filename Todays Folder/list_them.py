import os
import pandas as pd

# Define the directory path
# directory = r"\\DESKTOP-92QEMPM\Stores\Inv - Quality Healthcare\April 2024"
directory = r"C:\Users\pc\Desktop\Inv - Quality Healthcare"



# Get all files in the directory
files = os.listdir(directory)

# Filter out PDF files
pdf_files = [file for file in files if file.endswith('.pdf')]

# Create an empty list to store extracted information
data = []

# Extract information from file names
for index, filename in enumerate(pdf_files):
    parts = filename.split('_')
    doc_id, date = parts[0].split('-')
    year = date[:4]
    month = date[4:]
    data.append({'Sno': index+1, 'Document ID': doc_id, 'Year': year, 'Month': month, 'Filename': filename})

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
