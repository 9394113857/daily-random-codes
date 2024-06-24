import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

# Paths
data_path = r"C:\Users\pc\Desktop\Inv - Quality Healthcare\May 2024 sheet data\data.xlsx"
invoice_dir = r"C:\Users\pc\Desktop\Inv - Quality Healthcare\May 2024 changes saved only"
pod_dir = r"C:\Users\pc\Desktop\Inv - Quality Healthcare\May 2024 changes with pods"
output_dir = r"C:\Users\pc\Desktop\Inv - Quality Healthcare\May 2024 Final Merged"

# Read Excel file
df = pd.read_excel(data_path)

# Counters for summary
total_processed = 0
total_skipped = 0
total_errors = 0

# Process each row in the Excel file
for index, row in df.iterrows():
    invoice_no = row['INVOICE NO']
    pod_no = row['POD NO']

    # Construct the invoice file path
    invoice_path = os.path.join(invoice_dir, f"{invoice_no}_2024-25.pdf")

    # Construct the POD file path
    pod_path = os.path.join(pod_dir, f"{pod_no}.pdf")

    # Construct the output file path
    output_path = os.path.join(output_dir, f"{invoice_no}_2024-25.pdf")

    # Check if the invoice file exists
    if not os.path.exists(invoice_path):
        print(f"Invoice file not found, skipping: {invoice_path}")
        total_skipped += 1
        continue

    # Check if the POD file exists
    if not os.path.exists(pod_path):
        print(f"POD file not found, skipping: {pod_path}")
        total_skipped += 1
        continue

    # Check if the merged file already exists
    if os.path.exists(output_path):
        print(f"Merged file already exists, skipping: {output_path}")
        total_skipped += 1
        continue

    # Merge the PDF files
    try:
        writer = PdfWriter()

        # Add invoice file pages
        invoice_reader = PdfReader(invoice_path)
        for page in invoice_reader.pages:
            writer.add_page(page)

        # Add POD file pages
        pod_reader = PdfReader(pod_path)
        for page in pod_reader.pages:
            writer.add_page(page)

        # Write the merged PDF to the output directory
        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)

        print(f"Merged {invoice_path} and {pod_path} into {output_path}")
        total_processed += 1

    except Exception as e:
        print(f"Error merging {invoice_path} and {pod_path}: {e}")
        total_errors += 1

print("Merging process completed.")
print(f"Total files processed: {total_processed}")
print(f"Total files skipped: {total_skipped}")
print(f"Total errors: {total_errors}")
