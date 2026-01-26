from time import sleep

def welcome_screen():
    print("Hello 👋🏻\nWelcome To The Secret Code Language UNIVERSE!\n")
    sleep(1)
    print("In This You Can Encode a Simple Sentence into a Sentence in a 'Secret Language'!\n")
    sleep(1)
    print("And You Can Decode It Too!\n")
    sleep(1)

def encode():
    code = input("Enter your message to encode: ")
    encoded_chars = []
    for i, char in enumerate(code):
        # Shift character by 3 positions and add position index for more complexity
        encoded_char = chr((ord(char) + 3 + i) % 256)
        encoded_chars.append(encoded_char)
    encoded_message = ''.join(encoded_chars)
    print("Encoded message:", encoded_message, "\n")
    sleep(1)


def decode():
    code = input("Enter your message to decode: ")
    decoded_chars = []
    for i, char in enumerate(code):
        # Reverse the encoding process
        decoded_char = chr((ord(char) - 3 - i) % 256)
        decoded_chars.append(decoded_char)
    decoded_message = ''.join(decoded_chars)
    print("Decoded message:", decoded_message, "\n")
    sleep(1)

def main():
    while True:
        welcome_screen()
        choice = input("Do you want to encode or decode or quit? (e/d/q): ").strip().lower()
        if choice == 'e':
            encode()
        elif choice == 'd':
            decode()
        elif choice == "q":
            print("Exiting... GOODBYE...", "\n"*3)
            sleep(1)
            break
        else:
            print("Invalid choice. Please enter 'e' for encode or 'd' for decode.", "\n"*3)
            sleep(1)


main()
