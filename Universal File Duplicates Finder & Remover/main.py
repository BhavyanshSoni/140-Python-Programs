import os
import hashlib

def file_hash(filepath, algo='md5', block_size=65536):
    hasher = hashlib.new(algo)
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def find_duplicates(folder_path):
    hashes = {}
    duplicates = []

    print(f"Scanning files in {folder_path}...")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                h = file_hash(full_path)
                if h in hashes:
                    duplicates.append((full_path, hashes[h]))
                else:
                    hashes[h] = full_path
            except Exception as e:
                print(f"Could not read {full_path}: {e}")

    return duplicates

def main():
    folder = input("Enter folder path to scan for duplicates: ").strip()
    if not os.path.exists(folder):
        print("Folder not found!")
        return

    duplicates = find_duplicates(folder)

    if not duplicates:
        print("No duplicates found!")
        return

    print("\nDuplicates found:")
    for i, (dup, orig) in enumerate(duplicates, 1):
        print(f"{i}. Duplicate: {dup}")
        print(f"   Original: {orig}\n")

    delete = input("Do you want to delete duplicates? (y/n): ").lower()
    if delete == 'y':
        for dup, orig in duplicates:
            try:
                os.remove(dup)
                print(f"Deleted: {dup}")
            except Exception as e:
                print(f"Error deleting {dup}: {e}")

if __name__ == "__main__":
    main()
