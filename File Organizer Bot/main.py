import os
import shutil

# Set folder to clean
target_folder = os.path.expanduser("~/Downloads")

# File type to folder mapping
file_types = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Music": [".mp3", ".wav"],
    "Setups": [".exe", ".msi", ".zip"]
}

# Create folders and move files
for file in os.listdir(target_folder):
    file_path = os.path.join(target_folder, file)

    if os.path.isfile(file_path):
        ext = os.path.splitext(file)[1].lower()
        moved = False

        for folder_name, extensions in file_types.items():
            if ext in extensions:
                dest_folder = os.path.join(target_folder, folder_name)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_folder, file))
                moved = True
                break

        if not moved:
            print(f"Skipping: {file}")
