import os
import shutil

def organize(folder_path):
    for filename in os.listdir(folder_path):
        src = os.path.join(folder_path, filename)
        if os.path.isfile(src):
            ext = filename.split('.')[-1].lower()
            dest_folder = os.path.join(folder_path, ext + "_files")
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(src, os.path.join(dest_folder, filename))

if __name__ == "__main__":
    path = input("Enter folder path to organize: ")
    organize(path)
    print("✅ Files organized by type!")