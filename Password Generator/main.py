import random

# Define character sets for password generation
symbols = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", ";", ":", "'", '"', "<", ">", ",", ".", "/", "?"]
numbers = [str(i) for i in range(100)]  # Convert numbers to strings
lowercase = [chr(i) for i in range(97, 123)]  # a-z
uppercase = [chr(i) for i in range(65, 91)]  # A-Z

while True:
    print("\n")
    print("Welcome To Password Generator!")
    print("|----------------------------|")
    print("|   Made By Bhavyansh Soni   |")
    print("|----------------------------|")
    print("In This Programme You Can Generate Passwords Of Any Length\n")



    try:
        length = int(input("Enter The Length Of Password: ")) 
        if length <= 0:
            print("Password Lenth Must Be Greater Than 0\n")
            break
        else:
            password = ''.join(random.choice(symbols + numbers + lowercase + uppercase) for i in range(length))
            print(f"Generated Password: {password}\n")

        generate_again = input("Want To Generate Again (y/n): ")
        if generate_again.lower() == "n":
            print("Exiting... GoodBye...\n")
            break

    except ValueError as v:
        print("Invalid Input! ❌\n")

