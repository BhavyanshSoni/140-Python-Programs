from time import sleep

def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To The Names Grouper!")
    s("Here you can Make a List in which you can make Seperate Groups and add Names to Them!")
    s("Let's Get Started!")
    name_of_list = input("\nName of List>> ")
    no_of_groups = int(input("\nNumber of Groups>> "))
    groups = []
    for i in range(no_of_groups):
        names = input(f"\nGroup {i+1} Names   Seperate names with(a Gap[ ])>> ")
        group = names.split(" ")
        groups.append(group)
    s("\n")
    j = 0
    for i in groups:
        j +=1
        for k in i:
            s(f"\nGroup {j}. {k}")
            
main()