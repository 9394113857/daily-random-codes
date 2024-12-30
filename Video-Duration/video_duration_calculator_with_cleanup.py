import os
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed
from moviepy.editor import VideoFileClip
from tabulate import tabulate

# Function to get video duration
def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)  # Load the video file using MoviePy
        duration = clip.duration  # Get the video duration in seconds
        clip.close()  # Close the video clip to free resources
        return duration  # Return the duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")  # Print any errors encountered
        return None  # Return None if there was an error

# Main class for the GUI Application
class VideoDurationApp:
    def __init__(self, root):
        self.root = root  # Store the main Tkinter window
        self.root.title("Video Duration Calculator")  # Set the window title
        self.video_data = []  # List to store video data (filename, duration)
        self.file_paths = []  # List to store paths of video files
        self.total_seconds = 0  # Variable to store total video duration
        self.page = 1  # Current page for pagination
        self.per_page = 10  # Number of videos to display per page

        # Create the UI elements
        self.create_widgets()

    def create_widgets(self):
        # Button to allow the user to select a directory
        self.select_button = tk.Button(self.root, text="Select Directory", font=('Arial', 12, 'bold'), command=self.select_directory)
        self.select_button.pack(pady=20)  # Place the button with some padding

        # Label to show selected path
        self.path_label = tk.Label(self.root, text="", font=('Arial', 10), wraplength=400)
        self.path_label.pack(pady=10)  # Place the label with some padding

        # Button to calculate video durations
        self.calculate_button = tk.Button(self.root, text="Calculate Total Duration", font=('Arial', 12, 'bold'), command=self.calculate_total_time, state=tk.DISABLED)
        self.calculate_button.pack(pady=20)  # Place the button with some padding

        # Frame to contain the pagination buttons
        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=10)  # Pack the frame with some padding

        # Previous button for pagination
        self.prev_button = tk.Button(self.navigation_frame, text="Previous", font=('Arial', 12), command=self.show_previous_page, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)  # Place the button to the left with some horizontal padding

        # Next button for pagination
        self.next_button = tk.Button(self.navigation_frame, text="Next", font=('Arial', 12), command=self.show_next_page, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)  # Place the button to the left with some horizontal padding

        # Exit button to quit the application
        self.exit_button = tk.Button(self.root, text="Exit", font=('Arial', 12, 'bold'), command=self.root.quit)
        self.exit_button.pack(pady=20)  # Place the button with some padding

    # Function to allow the user to select a directory
    def select_directory(self):
        folder_path = filedialog.askdirectory()  # Open a directory selection dialog
        if folder_path:  # If a folder is selected
            self.path_label.config(text=f"Selected Path: {folder_path}")  # Display the folder path in the label
            self.folder_path = folder_path  # Store the folder path
            self.calculate_button.config(state=tk.NORMAL)  # Enable the calculate button

    # Function to calculate total time of all videos in the selected folder
    def calculate_total_time(self):
        video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg']  # List of supported video file extensions
        self.file_paths = []  # Reset the list of video files

        # Walk through the folder and gather video file paths
        for root, dirs, files in os.walk(self.folder_path):  # Walk through all subdirectories and files
            for file in files:  # Check each file
                if file.split('.')[-1].lower() in video_extensions:  # Check if the file has a supported extension
                    self.file_paths.append(os.path.join(root, file))  # Add the file path to the list

        # Check if no video files were found
        if not self.file_paths:
            messagebox.showwarning("No Video Files Found", "No video files were detected in the selected directory.")  # Show a warning
            return  # Exit the function if no videos are found

        # Use ThreadPoolExecutor to calculate the duration of each video concurrently
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_video_duration, path) for path in self.file_paths]  # Submit tasks to the executor
            for i, future in enumerate(as_completed(futures)):  # Process completed tasks as they finish
                duration = future.result()  # Get the duration of the video
                if duration is not None:
                    hours = int(duration // 3600)  # Calculate hours
                    minutes = int((duration % 3600) // 60)  # Calculate minutes
                    seconds = int(duration % 60)  # Calculate seconds
                    self.video_data.append([i + 1, os.path.basename(self.file_paths[i]), f"{hours} hours, {minutes} minutes, {seconds} seconds", duration])  # Store the video data

        # Enable the next button if there is more than one page of data
        if len(self.video_data) > self.per_page:
            self.next_button.config(state=tk.NORMAL)
        self.show_page(self.page)  # Show the first page of video data

    # Function to display the current page of video data
    def show_page(self, page):
        start = (page - 1) * self.per_page  # Calculate the starting index for the page
        end = start + self.per_page  # Calculate the ending index for the page
        data_to_display = self.video_data[start:end]  # Get the data for the current page

        # Calculate the total and average duration
        total_duration = sum([video[3] for video in self.video_data])  # Sum the durations of all videos
        average_duration = total_duration / len(self.video_data) if self.video_data else 0  # Calculate the average duration

        # Convert total and average duration to hours, minutes, seconds
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

        # Table headers for the video list
        table_headers = ["S.No", "Video File", "Duration"]
        formatted_table = tabulate(data_to_display, headers=table_headers, tablefmt="grid")  # Format the video data as a table

        # Create a new window to show the video data in tabular form
        result_window = tk.Toplevel(self.root)  # Create a new top-level window
        result_window.title(f"Page {page}")  # Set the window title

        # Display the formatted table
        table_label = tk.Label(result_window, text=formatted_table, font=('Courier', 10), justify=tk.LEFT)
        table_label.pack(padx=10, pady=10)  # Pack the label with some padding

        # Display the summary at the bottom
        summary_frame = tk.Frame(result_window)  # Create a frame for the summary
        summary_frame.pack(pady=10)  # Pack the frame with some padding

        summary_label = tk.Label(summary_frame, text="Summary:", font=('Arial', 12, 'bold'))  # Title for the summary
        summary_label.pack()  # Pack the label

        # Display each row of the summary
        for row in summary:
            summary_text = f"{row[0]}: {row[1]}"  # Create the summary text
            summary_row = tk.Label(summary_frame, text=summary_text, font=('Arial', 10))  # Create a label for the summary row
            summary_row.pack()  # Pack the summary row label

        # Enable/disable the prev and next buttons based on the page number
        if page == 1:
            self.prev_button.config(state=tk.DISABLED)  # Disable the "Previous" button on the first page
        else:
            self.prev_button.config(state=tk.NORMAL)  # Enable the "Previous" button

        if end >= len(self.video_data):
            self.next_button.config(state=tk.DISABLED)  # Disable the "Next" button if we're on the last page
        else:
            self.next_button.config(state=tk.NORMAL)  # Enable the "Next" button

    # Function to show the next page of data
    def show_next_page(self):
        self.page += 1  # Increment the page number
        self.show_page(self.page)  # Show the next page

    # Function to show the previous page of data
    def show_previous_page(self):
        self.page -= 1  # Decrement the page number
        self.show_page(self.page)  # Show the previous page

# Main function to run the Tkinter application
def main():
    root = tk.Tk()  # Create the main Tkinter window
    app = VideoDurationApp(root)  # Create an instance of the VideoDurationApp class
    root.mainloop()  # Run the Tkinter event loop

# Check if the script is being run directly and start the application
if __name__ == "__main__":
    main()  
