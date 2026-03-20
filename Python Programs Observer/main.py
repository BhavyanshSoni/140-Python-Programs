from time import sleep
from os import *

def s(txt, d=0.02):
    for i in txt:
        print(i, end='', flush=True)
        sleep(d)
    print()

def welcome():
    s("Welcome to Python Programs Observer! --> Made by 'Bhavyansh Soni'")
    s("\nHere, you can check out all of my 141 Programs!")
    s("So, Let's Get Started\n")



welcome()