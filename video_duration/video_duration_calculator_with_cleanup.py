from concurrent.futures import ThreadPoolExecutor, as_completed
from moviepy.editor import VideoFileClip
import os
from tabulate import tabulate

def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def calculate_total_time(folder_path):
    video_data = []
    total_seconds = 0
    total_files = 0
    video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg']
    sno = 1
    file_paths = []

    # Collect all video file paths
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.split('.')[-1].lower() in video_extensions:
                file_paths.append(os.path.join(root, file))

    # Process video files concurrently
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_video_duration, path) for path in file_paths]
        for future in as_completed(futures):
            duration = future.result()
            if duration is not None:
                total_seconds += duration
                total_files += 1
                hours = int(duration // 3600)
                minutes = int((duration % 3600) // 60)
                seconds = int(duration % 60)
                video_data.append([sno, os.path.basename(file_paths[total_files - 1]), f"{hours} hours, {minutes} minutes, {seconds} seconds"])
                sno += 1

    total_hours = int(total_seconds // 3600)
    total_minutes = int((total_seconds % 3600) // 60)
    total_seconds_remainder = int(total_seconds % 60)

    video_data.append(["Total", "", f"{total_hours} hours, {total_minutes} minutes, {total_seconds_remainder} seconds"])

    if total_files != 0:
        average_duration_seconds = total_seconds / total_files
        average_minutes = int(average_duration_seconds // 60)
        average_seconds = int(average_duration_seconds % 60)
        average_duration_formatted = f"{average_minutes} minutes, {average_seconds} seconds"
    else:
        average_duration_formatted = "N/A"

    video_data.append(["Average", "", average_duration_formatted])

    table_headers = ["S.No", "Video File", "Duration"]
    print("Total Duration of All Video Files:")
    print(tabulate(video_data, headers=table_headers, tablefmt="grid"))

def main():
    path = input("Please enter the path to the directory containing video files: ")
    if not os.path.exists(path):
        print("Invalid path!")
        return
    calculate_total_time(path)

if __name__ == "__main__":
    main()
