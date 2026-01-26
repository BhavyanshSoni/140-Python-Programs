from time import sleep

def s(txt, delay=0.03):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To ID Card Generator!")
    s("In this you will add Address, Name and DOB(Date of Birth), etc.!")
    s("And the Proramme will generate an ID Card!")
    s("Let's Get Started!")
    try:
        name = input("\nName>> ")
        class_room = int(input("\nEnter Class like(1, 2,... 12)>> "))
        Section = input("\nSection>> ")
        Address = input("\nAddress>> ")
        father_name = input("\nFather Name>> ")
        mother_name = input("\nMother Name>> ")
        Birth_Year = input("\n\nBirth Year>> ")
        Birth_mon = input("Birth Month>> ")
        Birth_day = input("Birth Day>> ")
        s("\n\n\n\tSAVED SUCCESSFULLY!")
        s(f"\n\t\tName -> {name}")
        s(f"\t\tFather's Name -> {father_name}")
        s(f"\t\tMother's Name -> {mother_name}")
        s(f"\t\tClass -> {class_room} {Section}")
        s(f"\t\tDOB -> {Birth_day}/{Birth_mon}/{Birth_Year}")
        s(f"\t\tAddress -> {Address}")
        s("\n\n\nThanks for Using this... GoodBye...")
        exit()
    except ValueError:
        s("Invalid Class!")
    

main()