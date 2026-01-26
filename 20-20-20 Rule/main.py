from time import sleep # This module is imported from time to send notification in every 20 minutes.
from plyer import notification # This module is imported from plyer to send notification.

# This is the main function which sends notification and then sleeps for 20 minutes.
def notify(): 

    # This interval time is set to 1200 seconds(20 Minutes).
    INTERVAL = 1200 

    # Using while True to make this program run until you turn off the device.
    while True: 

        # This is the area where message and title is set.
        notification.notify( 
            title = "Bhavyansh Look at something 20 feet away from you",
            message = "Look 👀 bro for 20 🕖 seconds after 20 ⏳ minutes i'll come again! 😎",
            timeout = 10 # This line keeps the notification for 10 seconds. So you can't ignore it.
        )

        # Here when the notification is sent program stops for 20 minutes.
        sleep(INTERVAL)

notify() 
# 👆🏻 Calling notify(Function).