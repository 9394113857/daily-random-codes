import win32evtlog
import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- CONFIG ---------------- #
EVENT_DETAILS = {
    6005: ("System Startup", "Windows started normally"),
    6006: ("System Shutdown", "Windows shut down properly"),
    41:   ("Unexpected Restart", "System restarted due to power failure or force restart"),
    6008: ("Unexpected Shutdown", "System shut down unexpectedly")
}

# Fixed export base path
EXPORT_BASE_PATH = os.path.join("PDF-Works", "System_Log_Exports")

# ---------------- LOG READER ---------------- #
def read_event_logs(year, month):
    server = 'localhost'
    log_type = 'System'
    handle = win32evtlog.OpenEventLog(server, log_type)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    temp_records = []

    while True:
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events:
            break

        for event in events:
            event_id = event.EventID
            if event_id in EVENT_DETAILS:
                event_time = event.TimeGenerated
                if event_time.year == year and event_time.month == month:
                    event_type, event_meaning = EVENT_DETAILS[event_id]

                    temp_records.append([
                        event_time,
                        event_time.strftime("%Y-%m-%d"),
                        event_time.strftime("%H:%M:%S"),
                        event_type,
                        event_id,
                        event_meaning
                    ])

    # Sort by actual datetime (oldest → newest)
    temp_records.sort(key=lambda x: x[0])

    # Add serial numbers
    final_records = []
    sno = 1
    for rec in temp_records:
        final_records.append([
            sno,
            rec[1],
            rec[2],
            rec[3],
            rec[4],
            rec[5]
        ])
        sno += 1

    return final_records

# ---------------- CSV EXPORT ---------------- #
def export_csv(data, year, month):
    # Ensure base export folder exists
    if not os.path.exists(EXPORT_BASE_PATH):
        os.makedirs(EXPORT_BASE_PATH)

    # Ensure YEAR folder exists
    year_folder = os.path.join(EXPORT_BASE_PATH, str(year))
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"System_Log_Report_{year}_{month}_{timestamp}.csv"
    filepath = os.path.join(year_folder, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "S.No",
            "Date",
            "Time",
            "Event Type",
            "Event ID",
            "Event Meaning"
        ])
        writer.writerows(data)

    return filepath

# ---------------- GUI ACTION ---------------- #
def generate_report():
    try:
        year = int(year_entry.get())
        month = int(month_entry.get())

        if month < 1 or month > 12:
            raise ValueError

        data = read_event_logs(year, month)

        if not data:
            messagebox.showinfo(
                "No Data",
                "No system ON/OFF related logs found for the selected month/year."
            )
            return

        # Clear table
        for row in tree.get_children():
            tree.delete(row)

        # Fill table
        for record in data:
            tree.insert("", tk.END, values=record)

        filepath = export_csv(data, year, month)

        messagebox.showinfo(
            "Export Successful",
            f"All system ON/OFF logs exported successfully:\n{filepath}"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid Year (YYYY) and Month (1–12)."
        )

# ---------------- GUI WINDOW ---------------- #
root = tk.Tk()
root.title("Windows System Daily ON / OFF Log Report")
root.geometry("1050x550")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Year (YYYY):").grid(row=0, column=0, padx=5)
year_entry = tk.Entry(frame, width=10)
year_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Month (1-12):").grid(row=0, column=2, padx=5)
month_entry = tk.Entry(frame, width=10)
month_entry.grid(row=0, column=3, padx=5)

tk.Button(
    frame,
    text="Generate & Export CSV",
    command=generate_report,
    bg="#4CAF50",
    fg="white"
).grid(row=0, column=4, padx=10)

columns = (
    "S.No",
    "Date",
    "Time",
    "Event Type",
    "Event ID",
    "Event Meaning"
)

tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=165, anchor="center")

tree.pack(pady=10)

tk.Button(
    root,
    text="Close",
    command=root.destroy,
    bg="#f44336",
    fg="white",
    width=15
).pack(pady=5)

root.mainloop()
