from time import sleep

def s(txt, d=0.01):
    for char in txt:
        print(char, end='', flush=True)
        sleep(d)
    print()

def welcome():
    s('WELCOME to "Street Figter 5!"')
    s("In this game you have to defeat 5 Bosses!")
    s("If you defeat them you'll win the game!")
    s("Let's Get Started!\n\n")

def train():
    global new_pwr_lvl
    s("Let's Train!")
    with open("power_lvl.txt") as f:
        power_lvl = int(f.read())
    new_pwr_lvl = int(power_lvl)
    for i in range(10):
        train_key = input("Press Any Key to Train... ")
        power_lvl += 1000
    with open("power_lvl.txt","w") as f:
        f.write(str(power_lvl))

def fight():
    with open("defeated_bosses.txt") as f:
        defeated_bosses = int(f.read())
    bosses = {
        "Boss 1":10000,
        "Boss 2":20000,
        "Boss 3":50000,
        "Boss 4":80000,
        "Boss 5":100000,
    }
    if new_pwr_lvl < 10000:
        s("Can't Fight With Boss 1")
    elif new_pwr_lvl >= 10000:
        s("Fighting With Boss 1")
        print("FIGHTING", end='', flush=True)
        s("...",2)
        s("\nYou Won")
        defeated_bosses += 1
    
    if new_pwr_lvl < 2:
        s("Can't Fight With Boss 2")
    elif new_pwr_lvl >= 20000:
        s("Fighting With Boss 2")
        print("FIGHTING", end='', flush=True)
        s("...",2)
        s("\nYou Won")
        defeated_bosses += 1
    
    if new_pwr_lvl < 50000:
        s("Can't Fight With Boss 3")
    elif new_pwr_lvl >= 50000:
        s("Fighting With Boss 3")
        print("FIGHTING", end='', flush=True)
        s("...",2)
        s("\nYou Won")
        defeated_bosses += 1
    
    if new_pwr_lvl < 80000:
        s("Can't Fight With Boss 4")
    elif new_pwr_lvl >= 80000:
        s("Fighting With Boss 4")
        print("FIGHTING", end='', flush=True)
        s("...",2)
        s("\nYou Won")
        defeated_bosses += 1
    
    if new_pwr_lvl < 100000:
        s("Can't Fight With Boss 5")
    elif new_pwr_lvl >= 100000:
        s("Fighting With Boss 5")
        print("FIGHTING", end='', flush=True)
        s("...",2)
        s("\nYou Won")
        defeated_bosses += 1

    with open("defeated_bosses.txt", "w") as f:
        f.write(str(defeated_bosses))

def see_power_lvl():
    with open("power_lvl.txt") as f:
        user_power_lvl = int(f.read())
    s(f"\nYour Power Level is: {user_power_lvl}")

def main():
    while True:
        s("\nWhat do you want to do?")
        s("1. Train to Get Power Level!")
        s("2. Fight with Bosses!")
        s("3. See your Power Level!")
        s("4. Exit!")
        try:
            ask = int(input("\n(1/4)>> "))
            if ask == 1:
                train()
            elif ask == 2:
                fight()
            elif ask == 3:
                see_power_lvl()
        except ValueError:
            s("Invalid! Choice")

main()