from random import randint

passwords = []
cracks = {}

try:
    digit = int(input("Enter Digits Of Password (4-6): "))
    
    if digit == 4:
        start = 1000
        end = 9999
    elif digit == 6:
        start = 100000
        end = 999999
    else:
        print("Only 4 and 6 Digits Are Allowed ❌")
        exit()

    # Generate 1000 random passwords
    for i in range(1000):
        passwords.append(randint(start, end))

    # Try cracking each password
    for item in passwords:
        attempts = 0
        while True:
            attempts += 1
            guess = randint(start, end)
            if guess == item:
                cracks[item] = attempts
                break

    # Print each result
    for password, tries in cracks.items():
        print(f"Password {password} cracked in {tries} tries.")

    # Find strongest password
    strongest_pass = max(cracks, key=cracks.get)
    print("\n💪 Strongest Password:")
    print(f"Password {strongest_pass} took {cracks[strongest_pass]} attempts to crack.")

except ValueError:
    print("Invalid! Digit Must Be Integer ❌")
