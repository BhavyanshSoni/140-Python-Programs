import shutil
import os
from datetime import datetime

def backup_folder(src_folder, backup_dir="backups"):
    if not os.path.exists(src_folder):
        print("Source folder does not exist.")
        return
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(os.path.normpath(src_folder))
    backup_path = os.path.join(backup_dir, f"{base_name}_backup_{timestamp}")
    shutil.make_archive(backup_path, 'zip', src_folder)
    print(f"Backup created at {backup_path}.zip")

def main():
    print("=== Project Backup Tool ===")
    src = input("Enter folder path to backup: ")
    backup_folder(src)

if __name__ == "__main__":
    main()
