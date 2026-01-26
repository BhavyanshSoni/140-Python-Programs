import time
from colorama import init, Fore, Style
class Employee:
    def __init__(self):
        print("Welcome To Resume Builder!")
        print("|==========================|")
        print("|  MADE BY BHAVYANSH SONI  |")
        print("|==========================|")

        # Taking Details From The User:
        name = input("Enter Your Name: ")
        language = input("Enter Which Programming Language You Want To Work In: ")
        education = input("Enter Your Education: ")
        projects_site = input("Enter Your Github Account Username To See Your Projects: ")
        e_mail = input("Enter Your E-Mail: ")

        print("|===================================|")
        print(f"| NAME: {name} |")
        print(f"| LANGUAGE: {language} |")
        print(f"| EDUCATION: {education} |")
        print(f"| GITHUB USERNAME: {projects_site} |")
        print(f"| E-MAIL: {e_mail} |")
        print("|===================================|")

    def main():
        init(autoreset=True)
        print(Fore.CYAN + "Welcome To Resume Builder!")
        print(Fore.YELLOW + "|==========================|")
        print(Fore.YELLOW + "|  MADE BY BHAVYANSH SONI  |")
        print(Fore.YELLOW + "|==========================|")

        # Taking Details From The User:
        name = input(Fore.GREEN + "Enter Your Name: ")
        language = input(Fore.GREEN + "Enter Which Programming Language You Want To Work In: ")
        education = input(Fore.GREEN + "Enter Your Education: ")
        projects_site = input(Fore.GREEN + "Enter Your Github Account Username To See Your Projects: ")
        e_mail = input(Fore.GREEN + "Enter Your E-Mail: ")

        print(Fore.MAGENTA + "|===================================|")
        print(Fore.MAGENTA + f"| NAME: {Fore.WHITE}{name}{Fore.MAGENTA} |")
        print(Fore.MAGENTA + f"| LANGUAGE: {Fore.WHITE}{language}{Fore.MAGENTA} |")
        print(Fore.MAGENTA + f"| EDUCATION: {Fore.WHITE}{education}{Fore.MAGENTA} |")
        print(Fore.MAGENTA + f"| GITHUB USERNAME: {Fore.WHITE}{projects_site}{Fore.MAGENTA} |")
        print(Fore.MAGENTA + f"| E-MAIL: {Fore.WHITE}{e_mail}{Fore.MAGENTA} |")
        print(Fore.MAGENTA + "|===================================|")

        print(Fore.CYAN + "Thank You For Using Resume Builder!")
        print(Fore.CYAN + "Your Resume Is Ready To Be Downloaded!")
        print(Fore.CYAN + "You Can Find It In The Same Folder As This Program!")
        print(Fore.CYAN + "Have A Nice Day!")
        print(Fore.YELLOW + "Please Wait For A Few Seconds...")
        time.sleep(3)
        print(Fore.RED + "Exiting... GoodBye...")

    if __name__ == "__main__":
        main()