from time import sleep

def s(txt, delay=0.02):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To Phone 📞 Number Saver!")
    s("Here you can Save phone numbers of your Family, Friends, etc!")
    s("Let's Get Started!")
    name = input("\nEnter Name of the Person>> ")
    phone_no = int(input("Phone 📞 Number>> "))
    if phone_no > 10 or phone_no < 1:
        s("Invalid Phone 📞 Number ❌")
    else:
        s(f"\n\n Name ->\t{name}")
        s("Phone No")