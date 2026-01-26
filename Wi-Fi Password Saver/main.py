from time import sleep

def s(txt, delay=0.02):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome to Wi-Fi Password Saver!")
    s("Here you can save Wi-Fi Passwords")
    s("Let's Get Started!")
    wifi_name = input("\nWi-Fi Name>> ")
    password = input("\nPassword>> ")
    s("\n\n\tSAVED ✅ Successfully!")
    s("\n\n\nThanks for using this program... GoodBye...")
    exit()

main()
