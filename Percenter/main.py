from time import sleep

def s(txt, delay=0.02):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome to The percenter!")
    s("Here you can See your Exam 📝 percentage by enter your Obtained Marks and total Marks!")
    s("Let's Get Started!")
    while True:
        try:
            total_marks = int(input("\nTotal Marks>> "))
            obtained_marks = int(input("Marks Obtained>> "))
            if total_marks < obtained_marks:
                s("Obtained Marks are Greater than Total Marks!\nInvalid!")
            else:
                print("\nCalculating Percentage", end='', flush=True)
                s("...",1.5)
                percentage = (obtained_marks/total_marks) * 100
                s(f"\nYou Achieved: {percentage} Percent")
            again = input("\nWant to Calculate Again(Y/N)>> ")
            if again.lower() == "y":
                s("\n")
            elif again.lower() == "n":
                s("Thanks for Using this Programme... GoodByee...")
                break
            else:
                s("Invalid Choice\nChoose From (Y/N)\n")
        except ValueError:
            s("Invalid Number of Marks\nTry Again")   


main()