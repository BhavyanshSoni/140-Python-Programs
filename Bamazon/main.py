from time import sleep # <- Time module is imported to support slow print(Function) In this Programme 😀.

def s(txt,delay=0.04): # <- This is the slow print Function 😁.
    for c in txt: # <- For loop is used to define every letter in the text as c.
        print(c, end='', flush=True)
        sleep(delay)
    print() # This line prints blank.

# This function displays the welcome screen(at starting) of the Programme.
def welcome():
    s("Welcome To Bamazon!")
    s("In This App you can order anything!")
    s("Let's Get Started!\n")

# This is the order(Function) used to display items available in stock and let the user order one of them.
def order():
    s("\nLet's Order Something!")
    items = { # This is the items(Dictonary) with their prices as values and items as Keys.
        "Soap":9,
        "Salt Packet":99,
        "Cake": 749,
        "Tooth Paste":59,
        "Tooth Brush":19,
        "TV": 44999,
        "Laptop": 19999,
        "T-Shirt":499,
        "Pants":499,
        "School Bag":999
    }
    s("What do you want to buy!")
    j = 0
    for i in items: # This for loop displays items available in stock on the display.
        j += 1
        s(f"{j}. {i} - Price: {items[i]}")
    print("\n")

    buy_item = input(f"which item(1/{len(items)})>> ") # This line take input from the user to ask what to order.
    if buy_item not in items.keys():
        s("This item isn't available! Sorry!\n")
        exit() # Exiting, if the item ordered by the user is available or not?
    else:
        no_of_item = int(input(f"How many of {buy_item} you want to buy: ")) # This line take input from the user to enter the quantity of items user want to buy?
        s(f"\nYour order is {no_of_item} {buy_item} with a Price of {items[buy_item] * no_of_item}\n")
        with open("order_list.txt", "a") as f: # Appending every order to a file named 'order_list.txt'.
            f.write(f"----------------Order----------------\nItems: {buy_item}\nQuantity {no_of_item}\nTotal Price: {items[buy_item] * no_of_item}\n------------------------------------\n\n")

# This is the menu(Function).
def menu():
    while True: # While True is used to run the menu Section infinite times. Until user chooses to exit!
        s("What Do you want to do?")
        s("1. Order Something!")
        s("2. Exit!\n")
        ask = int(input("(1/3)>> "))
        if ask == 1:
            order()
        elif ask == 2:
            s("Thanks For Using Bamazon 🛒. GoodBye...")
            break
        
menu()
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------END------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------