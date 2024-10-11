import os
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed
from moviepy.editor import VideoFileClip
from tabulate import tabulate

# Cell 1: Function to get video duration
def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Cell 2: Main class for the GUI Application
class VideoDurationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Duration Calculator")  # Set the window title
        self.video_data = []  # Stores video data for displaying
        self.file_paths = []  # Stores the file paths of video files
        self.total_seconds = 0  # Stores total duration in seconds
        self.page = 1  # Pagination current page
        self.per_page = 10  # Number of rows per page
        
        # Cell 3: Adding widgets for user interaction
        self.create_widgets()

    # Cell 4: Function to create the UI elements
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

    # Cell 5: Function to select directory and enable calculation button
    def select_directory(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_label.config(text=f"Selected Path: {folder_path}")
            self.folder_path = folder_path
            self.calculate_button.config(state=tk.NORMAL)  # Enable the calculate button

    # Cell 6: Function to calculate total and average video duration
    def calculate_total_time(self):
        video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg']
        self.file_paths = []
        self.video_data.clear()
        self.total_seconds = 0

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
                    self.total_seconds += duration
                    hours = int(duration // 3600)
                    minutes = int((duration % 3600) // 60)
                    seconds = int(duration % 60)
                    self.video_data.append([i + 1, os.path.basename(self.file_paths[i]), f"{hours} hours, {minutes} minutes, {seconds} seconds"])

        # Calculate total and average duration
        total_hours = int(self.total_seconds // 3600)
        total_minutes = int((self.total_seconds % 3600) // 60)
        total_seconds = int(self.total_seconds % 60)

        # Calculate average duration if there are any videos
        if len(self.video_data) > 0:
            average_duration = self.total_seconds / len(self.video_data)
            avg_hours = int(average_duration // 3600)
            avg_minutes = int((average_duration % 3600) // 60)
            avg_seconds = int(average_duration % 60)
        else:
            avg_hours = avg_minutes = avg_seconds = 0

        self.total_duration_str = f"Total Duration: {total_hours} hours, {total_minutes} minutes, {total_seconds} seconds"
        self.avg_duration_str = f"Average Duration: {avg_hours} hours, {avg_minutes} minutes, {avg_seconds} seconds"

        # Enable the next button if there is more than one page of data
        if len(self.video_data) > self.per_page:
            self.next_button.config(state=tk.NORMAL)

        # Display the results
        self.show_page(self.page)

    # Cell 7: Function to display the current page of video data
    def show_page(self, page):
        start = (page - 1) * self.per_page
        end = start + self.per_page
        data_to_display = self.video_data[start:end]

        table_headers = ["S.No", "Video File", "Duration"]
        formatted_table = tabulate(data_to_display, headers=table_headers, tablefmt="grid")

        # Create a new window to show the video data in tabular form
        result_window = tk.Toplevel(self.root)
        result_window.title(f"Page {page}")

        # Display the total and average durations
        total_duration_label = tk.Label(result_window, text=self.total_duration_str, font=('Arial', 12, 'bold'))
        total_duration_label.pack(pady=10)

        avg_duration_label = tk.Label(result_window, text=self.avg_duration_str, font=('Arial', 12, 'bold'))
        avg_duration_label.pack(pady=10)

        result_label = tk.Label(result_window, text=formatted_table, font=('Courier', 10), justify=tk.LEFT)
        result_label.pack()

        # Enable/disable the prev and next buttons based on the page number
        if page == 1:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if end >= len(self.video_data):
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    # Cell 8: Function to show the next page of data
    def show_next_page(self):
        self.page += 1
        self.show_page(self.page)

    # Cell 9: Function to show the previous page of data
    def show_previous_page(self):
        self.page -= 1
        self.show_page(self.page)

# Cell 10: Main function to run the Tkinter application
def main():
    root = tk.Tk()
    app = VideoDurationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
