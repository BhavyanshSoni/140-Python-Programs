from time import sleep
import os

def s(text,delay=0.000001):
    for char in text:
        print(char, end = '', flush=True)
        sleep(delay)
    print()

def welcome_screen():
    s("Welcome To Blog Uploader!")
    s("Here You can upload your own blogs!")
    s("Let's Get Started")


def write_blog():
    global author
    s("Let's Write Your Blog!")
    blog = input("\n")
    s("Author: ")
    author = input(">> ")
    with open(f"{author}_Blog.txt", "w") as f:
        f.write(blog)

def explore_blogs():
    
    blogs = os.listdir("E:\\Python Programmes\\Blog Uploader")
    j = 0
    if len(blogs) >= 1:
        s("\nNo Blogs Sorry!")
        s("You Should Make Some!")
    else:
        s("Blogs: ")
        for i in blogs:
            j = j + 1
            if ".txt" in i:
                with open(i) as f:
                    blog = f.read()
                    s(f"{j}. {blog}")
        

def menu():
    while True:
        s("\nWhat You Want To Do First: ")
        s("1. Upload Blog!")
        s("2. Explore Blogs")
        s("2. Exit!")
        try:
            action = int(input("(1-3)>> "))
            if action == 1:
                write_blog()
            elif action == 2:
                explore_blogs()
            elif action == 3:
                s("Exiting... GoodBye...")
                exit()    
        except ValueError as v:
            s("Invalid Action! Try Again ❌")
            exit()

welcome_screen()
menu()