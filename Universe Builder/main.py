from time import sleep # This Module(Time) is imported to support slow printing(Function) to make the programme more attractive.

# This is the slow print(Function) this Function split the txt in c and then it would attractively Print.
def s(txt,delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

# This is the Welcome screen of the Programme. 
def welcome():
    s("Welcome To The Planet Builder")
    s("In this you can make:")
    s("1. Shape of planet!")
    s("2. Name of planet!")
    s("3. Type of Living Organisms!")
    s("4. Type of Air!")
    s("5. Talking Language!")

# This is the main(Function) of the Programme.
def main():
    s("\nLet's Get Started!")
    shape = input("Enter How the Planet should look like? >> ")
    name = input("Name of the Planet >> ")
    liv_org = input("Enter which type of organisms should live in this planet? >> ")
    air = input("Enter Which Gas should the living organisms inhale to Live? >> ")
    lang = input("Enter Name of language in which they could Communicate? >> ")
    s("Saved Successfully ✅")
    s(f"\n--------------------{name.upper()}---------------------") # This print table 
    s(f"Shape - {shape}")
    s("-----------------------------------------------")
    s(f"Type of Organisms - {liv_org}")
    s("-----------------------------------------------")
    s(f"Type Of Air - {air}")
    s("-----------------------------------------------")
    s(f"Communication Language - {lang}")
    s("-----------------------------------------------")
    s("\n")

welcome()
main()

