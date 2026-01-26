from time import sleep

def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    name = input("Your Name>> ")
    s(f"\nWelcome Zoologist {name}!")
    s("In this Programme you can save Information of Animals!")
    s("Let's Get Started!\n")
    i = 0
    while True:
        i = i + 1
        s(f"\n----------Animal {i}----------\n")
        animal_name = input("Animal Name>> ")
        information = input(f"Information 'bout {animal_name}>> ")
        s("\n")
        s(f"Name -> {animal_name}")
        s(f"Information -> {information}")
        with open("animals.txt", "a") as f:
            f.write(f"------------------------------------------------------------------------------------------------------------------------------------------------\nName -> {animal_name}\nInformation -> {information}\n------------------------------------------------------------------------------------------------------------------------------------------------\n")
        again = input("\nWant to save Again(Y/N)>> ")
        if again.lower() == "n":
            s("\nGoodByee...Thanks for using this Programme...")
            break

main()