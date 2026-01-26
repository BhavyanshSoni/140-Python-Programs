import re

def password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    errors = [length_error, digit_error, uppercase_error, lowercase_error, symbol_error]
    score = errors.count(False)  # Count how many checks passed

    if score == 5:
        strength = "Strong"
    elif 3 <= score < 5:
        strength = "Medium"
    else:
        strength = "Weak"

    return strength, errors

def main():
    print("🔐 Password Strength Checker 🔐\n")
    password = input("Enter your password to check strength: ")

    strength, errors = password_strength(password)

    print(f"\nPassword Strength: {strength}")

    if strength != "Strong":
        print("Suggestions to improve your password:")
        if errors[0]:
            print("- Use at least 8 characters")
        if errors[1]:
            print("- Include at least one digit (0-9)")
        if errors[2]:
            print("- Include at least one uppercase letter (A-Z)")
        if errors[3]:
            print("- Include at least one lowercase letter (a-z)")
        if errors[4]:
            print("- Include at least one special character (!@#$%^&* etc.)")

if __name__ == "__main__":
    main()
