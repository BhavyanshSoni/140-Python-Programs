import os
import time
import json
import base64
import shutil
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass
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

class SecureFileLocker:
    def __init__(self):
        self.VAULT_DIR = "secure_vault"
        self.CONFIG_FILE = "vault_config.json"
        self.SALT_FILE = "vault.salt"
        self.config = {
            'password_hash': None,
            'locked_files': {}
        }
        self.fernet = None
        self.setup_vault()

    def display_welcome(self):
        """Display welcome screen with animation"""
        clear_screen()
        banner = """
╔═══════════════════════════════════════╗
║        Secure File Locker             ║
║         By: Bhavyansh Soni            ║
╚═══════════════════════════════════════╝
        """
        for line in banner.split('\n'):
            slow_print(Fore.CYAN + line + Style.RESET_ALL)
        time.sleep(1)

    def setup_vault(self):
        """Initialize the vault directory and configuration"""
        # Create vault directory if it doesn't exist
        if not os.path.exists(self.VAULT_DIR):
            os.makedirs(self.VAULT_DIR)

        # Load or create configuration
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                slow_print(f"{Fore.RED}Error loading configuration: {str(e)}{Style.RESET_ALL}")
                self.config = {'password_hash': None, 'locked_files': {}}

        # Load or generate salt
        if os.path.exists(self.SALT_FILE):
            with open(self.SALT_FILE, 'rb') as f:
                self.salt = f.read()
        else:
            self.salt = os.urandom(16)
            with open(self.SALT_FILE, 'wb') as f:
                f.write(self.salt)

    def save_config(self):
        """Save vault configuration"""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            slow_print(f"{Fore.RED}Error saving configuration: {str(e)}{Style.RESET_ALL}")

    def get_key_from_password(self, password):
        """Generate a Fernet key from a password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def set_password(self):
        """Set up the vault password"""
        while True:
            password = getpass(f"{Fore.GREEN}Enter new vault password: {Style.RESET_ALL}")
            confirm = getpass(f"{Fore.GREEN}Confirm password: {Style.RESET_ALL}")
            
            if password == confirm:
                if len(password) < 8:
                    slow_print(f"{Fore.RED}Password must be at least 8 characters long!{Style.RESET_ALL}")
                    continue
                    
                key = self.get_key_from_password(password)
                self.config['password_hash'] = base64.b64encode(key).decode()
                self.fernet = Fernet(key)
                self.save_config()
                slow_print(f"{Fore.GREEN}Password set successfully!{Style.RESET_ALL}")
                break
            else:
                slow_print(f"{Fore.RED}Passwords don't match! Try again.{Style.RESET_ALL}")

    def verify_password(self):
        """Verify the vault password"""
        if not self.config['password_hash']:
            slow_print(f"{Fore.YELLOW}No password set. Please set a password first.{Style.RESET_ALL}")
            self.set_password()
            return True

        attempts = 3
        while attempts > 0:
            password = getpass(f"{Fore.GREEN}Enter vault password ({attempts} attempts left): {Style.RESET_ALL}")
            key = self.get_key_from_password(password)
            
            if base64.b64encode(key).decode() == self.config['password_hash']:
                self.fernet = Fernet(key)
                return True
                
            attempts -= 1
            if attempts > 0:
                slow_print(f"{Fore.RED}Incorrect password! Please try again.{Style.RESET_ALL}")
            else:
                slow_print(f"{Fore.RED}Too many failed attempts. Access denied!{Style.RESET_ALL}")
                
        return False

    def lock_file(self):
        """Lock (encrypt) a file"""
        if not self.verify_password():
            return

        file_path = input(f"\n{Fore.CYAN}Enter path of file to lock: {Style.RESET_ALL}")
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found!")
                
            # Generate a unique ID for the file
            file_id = base64.b64encode(os.urandom(8)).decode()
            original_name = os.path.basename(file_path)
            encrypted_name = f"{file_id}.locked"
            
            # Read and encrypt the file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            encrypted_data = self.fernet.encrypt(file_data)
            
            # Save encrypted file
            encrypted_path = os.path.join(self.VAULT_DIR, encrypted_name)
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Store file info
            self.config['locked_files'][file_id] = {
                'original_name': original_name,
                'locked_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'original_path': os.path.abspath(file_path)
            }
            self.save_config()
            
            # Delete original file
            os.remove(file_path)
            
            slow_print(f"\n{Fore.GREEN}File locked successfully!{Style.RESET_ALL}")
            print(f"Original file: {original_name}")
            print(f"Locked file ID: {file_id}")
            
        except Exception as e:
            slow_print(f"\n{Fore.RED}Error locking file: {str(e)}{Style.RESET_ALL}")

    def unlock_file(self):
        """Unlock (decrypt) a file"""
        if not self.verify_password():
            return

        if not self.config['locked_files']:
            slow_print(f"\n{Fore.YELLOW}No locked files found!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Locked Files:{Style.RESET_ALL}")
        print("═" * 50)
        for file_id, info in self.config['locked_files'].items():
            print(f"ID: {file_id}")
            print(f"Name: {info['original_name']}")
            print(f"Locked on: {info['locked_time']}")
            print("─" * 50)

        file_id = input(f"\n{Fore.GREEN}Enter file ID to unlock: {Style.RESET_ALL}")
        
        try:
            if file_id not in self.config['locked_files']:
                raise ValueError("Invalid file ID!")
                
            file_info = self.config['locked_files'][file_id]
            encrypted_path = os.path.join(self.VAULT_DIR, f"{file_id}.locked")
            
            if not os.path.exists(encrypted_path):
                raise FileNotFoundError("Encrypted file not found in vault!")
            
            # Read and decrypt the file
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Save decrypted file
            original_path = file_info['original_path']
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Remove encrypted file and entry
            os.remove(encrypted_path)
            del self.config['locked_files'][file_id]
            self.save_config()
            
            slow_print(f"\n{Fore.GREEN}File unlocked successfully!{Style.RESET_ALL}")
            print(f"File restored to: {original_path}")
            
        except Exception as e:
            slow_print(f"\n{Fore.RED}Error unlocking file: {str(e)}{Style.RESET_ALL}")

    def view_locked_files(self):
        """View list of locked files"""
        if not self.config['locked_files']:
            slow_print(f"\n{Fore.YELLOW}No locked files found!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Locked Files:{Style.RESET_ALL}")
        print("═" * 50)
        
        for file_id, info in self.config['locked_files'].items():
            print(f"\n{Fore.GREEN}File ID: {file_id}{Style.RESET_ALL}")
            print(f"Original Name: {info['original_name']}")
            print(f"Original Path: {info['original_path']}")
            print(f"Locked Time: {info['locked_time']}")
            print("─" * 50)

    def change_password(self):
        """Change the vault password"""
        if not self.verify_password():
            return

        slow_print(f"\n{Fore.YELLOW}Changing vault password...{Style.RESET_ALL}")
        
        try:
            # Get new password
            while True:
                new_password = getpass(f"{Fore.GREEN}Enter new password: {Style.RESET_ALL}")
                confirm = getpass(f"{Fore.GREEN}Confirm new password: {Style.RESET_ALL}")
                
                if new_password == confirm:
                    if len(new_password) < 8:
                        slow_print(f"{Fore.RED}Password must be at least 8 characters long!{Style.RESET_ALL}")
                        continue
                    break
                else:
                    slow_print(f"{Fore.RED}Passwords don't match! Try again.{Style.RESET_ALL}")

            # Re-encrypt all files with new password
            new_key = self.get_key_from_password(new_password)
            new_fernet = Fernet(new_key)
            
            for file_id in self.config['locked_files']:
                encrypted_path = os.path.join(self.VAULT_DIR, f"{file_id}.locked")
                
                # Read current encrypted data
                with open(encrypted_path, 'rb') as f:
                    encrypted_data = f.read()
                
                # Decrypt with old key and re-encrypt with new key
                decrypted_data = self.fernet.decrypt(encrypted_data)
                new_encrypted_data = new_fernet.encrypt(decrypted_data)
                
                # Save re-encrypted data
                with open(encrypted_path, 'wb') as f:
                    f.write(new_encrypted_data)

            # Update configuration with new password hash
            self.config['password_hash'] = base64.b64encode(new_key).decode()
            self.fernet = new_fernet
            self.save_config()
            
            slow_print(f"\n{Fore.GREEN}Password changed successfully!{Style.RESET_ALL}")
            
        except Exception as e:
            slow_print(f"\n{Fore.RED}Error changing password: {str(e)}{Style.RESET_ALL}")

    def main_menu(self):
        """Main program loop"""
        while True:
            clear_screen()
            self.display_welcome()
            
            slow_print(f"\n{Fore.YELLOW}Options:{Style.RESET_ALL}")
            slow_print("1. Lock File")
            slow_print("2. Unlock File")
            slow_print("3. View Locked Files")
            slow_print("4. Change Password")
            slow_print("5. Exit")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice (1-5): {Style.RESET_ALL}")
            
            if choice == '1':
                self.lock_file()
            elif choice == '2':
                self.unlock_file()
            elif choice == '3':
                self.view_locked_files()
            elif choice == '4':
                self.change_password()
            elif choice == '5':
                slow_print(f"\n{Fore.YELLOW}Thank you for using Secure File Locker!{Style.RESET_ALL}")
                break
            else:
                slow_print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        locker = SecureFileLocker()
        locker.main_menu()
    except KeyboardInterrupt:
        clear_screen()
        slow_print(f"\n{Fore.YELLOW}Program terminated by user. Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        slow_print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")