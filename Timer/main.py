from time import *
from plyer import notification
print("Welcome To The Timer Made By Bhavyansh Soni!")
print("In This Programme You Can Set Timer!")

try:

    hour = int(input("Enter Hour in 24 Format: "))
    minute = int(input("Enter Minutes: "))
    second = int(input("Enter Seconds: "))
    print("Timer Has Been Set")
    current_hour = strftime("%H:")
    current_minute = strftime("%M:")
    current_second = strftime("%S")
    while  hour != current_hour and minute != current_minute and second != current_second:
        sleep(10)
    print("The Timer Rung 🛎")
    notification.notify(
        title = f"The Timer Has Been Rung!",
        message = "GO! Your Time Is Up!",
        timeout = 5
    )
except ValueError as v:
    print("Invalid Time!")