import os

print("Hi,\nWelcome To The BOOK BUILDER!")
print("Here You Can Make Books on your own of your choice!")
print("In this You Can:")
print("1. Set the names of book!")
print("2. Set the names of pages!")
print("3. You can add unlimited ♾ number of pages to your book!")
print("Now Let's Make a BOOK of your choice!")
print("\n"*3)

def build_book():
    i = 0
    while True:
        i = i + 1
        name = input("Enter Name Of BOOK: ")
        print(f"Starting To Build Book {name}\n Page No. {i}")
        page_name = input(f"Enter Name Of Page No. {i}: ")
        page = input("Start Typing: \n")
        os.makedirs(name)

        with open(f"{name}/{page_name} PAGE - {i}.txt", "w") as f:
            f.write(page)

        again = input("Want To Make More Pages (Y/N): ")  
        if again.lower() == "y":
            print("Making More PAGES...")
        elif again.lower() == "n":
            print("Thanks For Using My BOOK BUILDER")
            print("GoodBye...")
            break
        

build_book()