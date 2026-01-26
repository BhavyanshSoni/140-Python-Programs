from time import sleep
from os import makedirs, path

# Change this variable to set where the folders should be created.
# Example: BASE_PATH = r"E:\My Projects"
# Leave it as "." to use the current directory.
BASE_PATH = "E:\\Python Programmes\\"


def s(txt, delay=0.04):
    # Print an empty line before each message so outputs don't overlap or mix
    print()
    for i in txt:
        print(i, end="", flush=True)
        sleep(delay)
    # Final newline so the next print starts on a new line
    print()


def main():
    # Intro
    s("Welcome to Program Folder Maker --> Made by Bhavyansh Soni")
    s("In this program you can create a folder and name it as you want.")

    # Ask for folder name
    s("Enter the name of the folder: ", delay=0.01)
    folder_name = input().strip()

    if not folder_name:
        s("Folder name cannot be empty. Exiting...")
        return

    # Build full folder path using the base path
    full_folder_path = path.join(BASE_PATH, folder_name)

    # Create the folder (including any missing parent folders)
    try:
        makedirs(full_folder_path, exist_ok=False)
        s(f"Folder created successfully at: {full_folder_path}")
    except FileExistsError:
        s(f"Folder already exists. Using the existing folder at: {full_folder_path}")

    s(f"Folder name: {folder_name}", delay=0.01)

    # Ask for file name inside the folder
    s("Enter the name of the file to create inside the folder (for example: main.py): ", delay=0.01)
    file_name = input().strip()

    if not file_name:
        s("File name cannot be empty. Exiting...")
        return

    target_file_path = path.join(full_folder_path, file_name)

    # Ask user what to write in the file
    s("What do you want to write in the file?", delay=0.01)
    s("1) Use the same content as in code.txt")
    s("2) Write something else")
    s("Enter your choice (1 or 2): ", delay=0.01)
    choice = input().strip()

    if choice == "1":
        # Copy content from code.txt
        try:
            with open("code.txt", "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            s("code.txt was not found in the current directory. Exiting...")
            return

    elif choice == "2":
        # Let user type custom content (multi-line, finish with empty line)
        s("Type the content you want to put in the file.")
        s("When you are done, press Enter on an empty line to finish.")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        content = "\n".join(lines)
    else:
        s("Invalid choice. Exiting...")
        return

    # Write the content to the file inside the folder
    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    s(f"File '{file_name}' has been created inside folder '{folder_name}'.")


if __name__ == "__main__":
    main()