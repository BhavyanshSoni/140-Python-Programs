import math
import os
def save_to_history(entry):
    try:
        os.makedirs("logs", exist_ok=True)  # Ensure logs folder exists
        with open("logs/history.txt", "a") as f:
            f.write(entry + "\n")
    except PermissionError:
        print("⚠️ Could not save to history: Permission denied.")
    except Exception as e:
        print(f"⚠️ Could not save to history: {e}")

def add():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        result = x + y
        print("Result:", result)
        save_to_history(f"Add: {x} + {y} = {result}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def subtract():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        result = x - y
        print("Result:", result)
        save_to_history(f"Subtract: {x} - {y} = {result}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def multiply():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        result = x * y
        print("Result:", result)
        save_to_history(f"Multiply: {x} * {y} = {result}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def divide():
    try:
        x = float(input("Enter numerator: "))
        y = float(input("Enter denominator: "))
        if y == 0:
            print("Error: Division by zero!")
        else:
            result = x / y
            print("Result:", result)
            save_to_history(f"Divide: {x} / {y} = {result}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def square():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        result_x = x ** 2
        result_y = y ** 2
        print(f"Squares: {result_x}, {result_y}")
        save_to_history(f"Square: {x}^2 = {result_x}, {y}^2 = {result_y}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def square_root():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        if x < 0 or y < 0:
            print("Error: Cannot take square root of negative number!")
        else:
            result_x = math.sqrt(x)
            result_y = math.sqrt(y)
            print(f"Square roots: {result_x}, {result_y}")
            save_to_history(f"Square root: sqrt({x}) = {result_x}, sqrt({y}) = {result_y}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def cube():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        result_x = x ** 3
        result_y = y ** 3
        print(f"Cubes: {result_x}, {result_y}")
        save_to_history(f"Cube: {x}^3 = {result_x}, {y}^3 = {result_y}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def cube_root():
    try:
        x = float(input("Enter first number: "))
        y = float(input("Enter second number: "))
        result_x = math.copysign(abs(x) ** (1/3), x)
        result_y = math.copysign(abs(y) ** (1/3), y)
        print(f"Cube roots: {result_x}, {result_y}")
        save_to_history(f"Cube root: {x}^(1/3) = {result_x}, {y}^(1/3) = {result_y}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

def operation():
    while True:
        print("\n--- Simple Scientific Calculator ---")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Square")
        print("6. Square Root")
        print("7. Cube")
        print("8. Cube Root")
        print("9. Exit")

        try:
            op = int(input("Choose operation (1-9): "))
            if op == 1:
                add()
            elif op == 2:
                subtract()
            elif op == 3:
                multiply()
            elif op == 4:
                divide()
            elif op == 5:
                square()
            elif op == 6:
                square_root()
            elif op == 7:
                cube()
            elif op == 8:
                cube_root()
            elif op == 9:
                print("Thank you for using the calculator. Goodbye!")
                break
            else:
                print("Invalid option! Please choose between 1 and 9.")
        except ValueError:
            print("✖️ Oops! Invalid input. Please enter a number between 1 and 9.")

operation()
