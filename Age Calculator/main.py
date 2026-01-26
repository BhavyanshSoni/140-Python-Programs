import time
def welcome_screen():
    print("Welcome To Age Calculator\n---> Made By Bhavyansh Soni!")
    print("In This Age Calculator You Can Calculate 🧮 That How Old ⌛ Are You ❓")
    print("You Just Need To Enter Your Birth Year And Your Name!", "\n"*2)

def age_calculator(name, birth_year= int()):
    year = time.strftime("%Y")

    if birth_year == 2025 or birth_year >= 2025:
        print("Invalid Birth Year")

    else:
        age_string = ""
        age = (int(year) - birth_year)
        if age < 1:
            age_string = f"{name}, You Are {age} Years Old"
            print(age_string)
        else:
            age_string = f"{name}, You Are {age} Year Old"
            print(age_string)

welcome_screen()

while True:
    try:
        calculate_again = input("Want To Calculate (Y/N): ")

        if calculate_again.lower() == "y":
            name = input("Enter Your Name: ")
            birth_year = int(input("Enter Your Birth Year: "))
            age_calculator(name, birth_year)

        elif calculate_again.lower() == "n":
            print("Exiting... GoodBye...")
            break
        else:
            print("Invalid Enter (Y/N)!")

    except (ValueError, KeyboardInterrupt) as v:
        print("Invalid Birth Year!")
