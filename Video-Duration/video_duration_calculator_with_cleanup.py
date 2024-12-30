import os
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed
from moviepy.editor import VideoFileClip
from tabulate import tabulate

# Function to get video duration
def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Main class for the GUI Application
class VideoDurationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Duration Calculator")  # Set the window title
        self.video_data = []  # Stores video data for displaying
        self.file_paths = []  # Stores the file paths of video files
        self.total_seconds = 0
        self.page = 1  # Pagination current page
        self.per_page = 10  # Number of rows per page

        # Adding widgets for user interaction
        self.create_widgets()

    def create_widgets(self):
        # Button to allow the user to select a directory
        self.select_button = tk.Button(self.root, text="Select Directory", font=('Arial', 12, 'bold'), command=self.select_directory)
        self.select_button.pack(pady=20)

        # Label to show selected path
        self.path_label = tk.Label(self.root, text="", font=('Arial', 10), wraplength=400)
        self.path_label.pack(pady=10)

        # Button to calculate video durations
        self.calculate_button = tk.Button(self.root, text="Calculate Total Duration", font=('Arial', 12, 'bold'), command=self.calculate_total_time, state=tk.DISABLED)
        self.calculate_button.pack(pady=20)

        # Frame for navigation buttons (pagination)
        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=10)

        # Previous and Next buttons for pagination
        self.prev_button = tk.Button(self.navigation_frame, text="Previous", font=('Arial', 12), command=self.show_previous_page, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.navigation_frame, text="Next", font=('Arial', 12), command=self.show_next_page, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Exit button to quit the application
        self.exit_button = tk.Button(self.root, text="Exit", font=('Arial', 12, 'bold'), command=self.root.quit)
        self.exit_button.pack(pady=20)

    def select_directory(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_label.config(text=f"Selected Path: {folder_path}")
            self.folder_path = folder_path
            self.calculate_button.config(state=tk.NORMAL)  # Enable the calculate button

    def calculate_total_time(self):
        video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg']
        self.file_paths = []

        # Walk through the folder and gather video file paths
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.split('.')[-1].lower() in video_extensions:
                    self.file_paths.append(os.path.join(root, file))

        # Check if no video files were found
        if not self.file_paths:
            messagebox.showwarning("No Video Files Found", "No video files were detected in the selected directory.")
            return

        # Use ThreadPoolExecutor to calculate the duration of each video concurrently
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_video_duration, path) for path in self.file_paths]
            for i, future in enumerate(as_completed(futures)):
                duration = future.result()
                if duration is not None:
                    hours = int(duration // 3600)
                    minutes = int((duration % 3600) // 60)
                    seconds = int(duration % 60)
                    self.video_data.append([i + 1, os.path.basename(self.file_paths[i]), f"{hours} hours, {minutes} minutes, {seconds} seconds", duration])

        # Enable the next button if there is more than one page of data
        if len(self.video_data) > self.per_page:
            self.next_button.config(state=tk.NORMAL)
        self.show_page(self.page)

    def show_page(self, page):
        start = (page - 1) * self.per_page
        end = start + self.per_page
        data_to_display = self.video_data[start:end]

        # Calculate the total and average duration
        total_duration = sum([video[3] for video in self.video_data])
        average_duration = total_duration / len(self.video_data) if self.video_data else 0

        total_hours = int(total_duration // 3600)
        total_minutes = int((total_duration % 3600) // 60)
        total_seconds = int(total_duration % 60)

        average_hours = int(average_duration // 3600)
        average_minutes = int((average_duration % 3600) // 60)
        average_seconds = int(average_duration % 60)

        # Add summary information (Total and Average durations)
        summary = [
            ["Total Duration", f"{total_hours} hours, {total_minutes} minutes, {total_seconds} seconds"],
            ["Average Duration", f"{average_hours} hours, {average_minutes} minutes, {average_seconds} seconds"]
        ]

        table_headers = ["S.No", "Video File", "Duration"]
        formatted_table = tabulate(data_to_display, headers=table_headers, tablefmt="grid")

        # Create a new window to show the video data in tabular form
        result_window = tk.Toplevel(self.root)
        result_window.title(f"Page {page}")

        # Display the formatted table
        table_label = tk.Label(result_window, text=formatted_table, font=('Courier', 10), justify=tk.LEFT)
        table_label.pack(padx=10, pady=10)

        # Display the summary at the bottom
        summary_frame = tk.Frame(result_window)
        summary_frame.pack(pady=10)

        summary_label = tk.Label(summary_frame, text="Summary:", font=('Arial', 12, 'bold'))
        summary_label.pack()

        for row in summary:
            summary_text = f"{row[0]}: {row[1]}"
            summary_row = tk.Label(summary_frame, text=summary_text, font=('Arial', 10))
            summary_row.pack()

        # Enable/disable the prev and next buttons based on the page number
        if page == 1:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if end >= len(self.video_data):
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    def show_next_page(self):
        self.page += 1
        self.show_page(self.page)

    def show_previous_page(self):
        self.page -= 1
        self.show_page(self.page)

# Main function to run the Tkinter application
def main():
    root = tk.Tk()
    app = VideoDurationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
