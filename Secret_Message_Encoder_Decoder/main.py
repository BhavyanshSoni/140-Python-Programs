import base64
import time
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init()

def slow_print(text, delay=0.03):
    """Print text with a typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

class SecretMessageTool:
    def __init__(self):
        self.history = []
        self.HISTORY_FILE = "message_history.json"
        self.load_history()

    def display_welcome(self):
        """Display welcome screen with animation"""
        clear_screen()
        banner = """
╔═══════════════════════════════════════╗
║    Secret Message Encoder/Decoder      ║
║         By: Bhavyansh Soni            ║
╚═══════════════════════════════════════╝
        """
        for line in banner.split('\n'):
            slow_print(Fore.CYAN + line + Style.RESET_ALL)
        time.sleep(1)

    def load_history(self):
        """Load message history from file"""
        try:
            if os.path.exists(self.HISTORY_FILE):
                with open(self.HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            slow_print(f"{Fore.RED}Error loading history: {str(e)}{Style.RESET_ALL}")
            self.history = []

    def save_history(self):
        """Save message history to file"""
        try:
            with open(self.HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            slow_print(f"{Fore.RED}Error saving history: {str(e)}{Style.RESET_ALL}")

    def get_fernet_key(self, password):
        """Generate a Fernet key from a password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'secret_salt',  # In production, use a random salt and store it
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)

    def caesar_cipher(self, text, shift, decrypt=False):
        """Implement Caesar cipher encryption/decryption"""
        if decrypt:
            shift = -shift
        
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    def base64_encode_decode(self, text, decrypt=False):
        """Implement Base64 encoding/decoding"""
        try:
            if decrypt:
                return base64.b64decode(text.encode()).decode()
            return base64.b64encode(text.encode()).decode()
        except Exception:
            return None

    def fernet_encrypt_decrypt(self, text, password, decrypt=False):
        """Implement Fernet encryption/decryption"""
        try:
            f = self.get_fernet_key(password)
            if decrypt:
                return f.decrypt(text.encode()).decode()
            return f.encrypt(text.encode()).decode()
        except Exception:
            return None

    def encode_message(self):
        """Encode a message using selected method"""
        print(f"\n{Fore.YELLOW}Encoding Methods:{Style.RESET_ALL}")
        print("1. Caesar Cipher")
        print("2. Base64")
        print("3. Fernet (Secure)")
        
        method = input(f"\n{Fore.GREEN}Choose method (1-3): {Style.RESET_ALL}")
        message = input(f"{Fore.GREEN}Enter message to encode: {Style.RESET_ALL}")
        
        try:
            if method == '1':
                shift = int(input(f"{Fore.GREEN}Enter shift value (1-25): {Style.RESET_ALL}"))
                if not 1 <= shift <= 25:
                    raise ValueError("Shift must be between 1 and 25")
                    
                encoded = self.caesar_cipher(message, shift)
                method_name = f"Caesar (shift={shift})"
                
            elif method == '2':
                encoded = self.base64_encode_decode(message)
                method_name = "Base64"
                
            elif method == '3':
                password = input(f"{Fore.GREEN}Enter encryption password: {Style.RESET_ALL}")
                encoded = self.fernet_encrypt_decrypt(message, password)
                method_name = "Fernet"
                
            else:
                slow_print(f"{Fore.RED}Invalid method choice!{Style.RESET_ALL}")
                return
            
            if encoded:
                print(f"\n{Fore.CYAN}Encoded message:{Style.RESET_ALL}")
                print("═" * 50)
                print(encoded)
                print("═" * 50)
                
                # Add to history
                self.history.append({
                    'type': 'encode',
                    'method': method_name,
                    'original': message,
                    'result': encoded
                })
                self.save_history()
            else:
                slow_print(f"{Fore.RED}Encoding failed!{Style.RESET_ALL}")
                
        except ValueError as e:
            slow_print(f"{Fore.RED}Invalid input: {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            slow_print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

    def decode_message(self):
        """Decode a message using selected method"""
        print(f"\n{Fore.YELLOW}Decoding Methods:{Style.RESET_ALL}")
        print("1. Caesar Cipher")
        print("2. Base64")
        print("3. Fernet (Secure)")
        
        method = input(f"\n{Fore.GREEN}Choose method (1-3): {Style.RESET_ALL}")
        message = input(f"{Fore.GREEN}Enter message to decode: {Style.RESET_ALL}")
        
        try:
            if method == '1':
                shift = int(input(f"{Fore.GREEN}Enter shift value (1-25): {Style.RESET_ALL}"))
                if not 1 <= shift <= 25:
                    raise ValueError("Shift must be between 1 and 25")
                    
                decoded = self.caesar_cipher(message, shift, decrypt=True)
                method_name = f"Caesar (shift={shift})"
                
            elif method == '2':
                decoded = self.base64_encode_decode(message, decrypt=True)
                method_name = "Base64"
                
            elif method == '3':
                password = input(f"{Fore.GREEN}Enter decryption password: {Style.RESET_ALL}")
                decoded = self.fernet_encrypt_decrypt(message, password, decrypt=True)
                method_name = "Fernet"
                
            else:
                slow_print(f"{Fore.RED}Invalid method choice!{Style.RESET_ALL}")
                return
            
            if decoded:
                print(f"\n{Fore.CYAN}Decoded message:{Style.RESET_ALL}")
                print("═" * 50)
                print(decoded)
                print("═" * 50)
                
                # Add to history
                self.history.append({
                    'type': 'decode',
                    'method': method_name,
                    'original': message,
                    'result': decoded
                })
                self.save_history()
            else:
                slow_print(f"{Fore.RED}Decoding failed!{Style.RESET_ALL}")
                
        except ValueError as e:
            slow_print(f"{Fore.RED}Invalid input: {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            slow_print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

    def view_history(self):
        """View operation history"""
        if not self.history:
            slow_print(f"\n{Fore.YELLOW}No operations in history!{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}Operation History:{Style.RESET_ALL}")
        print("═" * 50)
        
        for entry in reversed(self.history[-10:]):  # Show last 10 entries
            print(f"{Fore.GREEN}{entry['type'].title()} using {entry['method']}:{Style.RESET_ALL}")
            print(f"Original: {entry['original']}")
            print(f"Result: {entry['result']}")
            print("─" * 50)

    def clear_history(self):
        """Clear operation history"""
        confirm = input(f"\n{Fore.RED}Are you sure you want to clear history? (y/n): {Style.RESET_ALL}")
        if confirm.lower() == 'y':
            self.history = []
            self.save_history()
            slow_print(f"{Fore.GREEN}History cleared successfully!{Style.RESET_ALL}")

    def main_menu(self):
        """Main program loop"""
        while True:
            clear_screen()
            self.display_welcome()
            
            slow_print(f"\n{Fore.YELLOW}Options:{Style.RESET_ALL}")
            slow_print("1. Encode Message")
            slow_print("2. Decode Message")
            slow_print("3. View History")
            slow_print("4. Clear History")
            slow_print("5. Exit")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice (1-5): {Style.RESET_ALL}")
            
            if choice == '1':
                self.encode_message()
            elif choice == '2':
                self.decode_message()
            elif choice == '3':
                self.view_history()
            elif choice == '4':
                self.clear_history()
            elif choice == '5':
                slow_print(f"\n{Fore.YELLOW}Thank you for using Secret Message Encoder/Decoder!{Style.RESET_ALL}")
                break
            else:
                slow_print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        tool = SecretMessageTool()
        tool.main_menu()
    except KeyboardInterrupt:
        clear_screen()
        slow_print(f"\n{Fore.YELLOW}Program terminated by user. Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        slow_print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}") 