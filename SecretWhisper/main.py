import base64
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
from datetime import datetime

# Initialize Rich console
console = Console()

class SecretWhisper:
    def __init__(self):
        self.messages_file = "whispers.enc"
        self.salt_file = "salt.bin"
        self.initialize_encryption()

    def initialize_encryption(self):
        """Initialize encryption with salt"""
        if os.path.exists(self.salt_file):
            with open(self.salt_file, 'rb') as f:
                self.salt = f.read()
        else:
            self.salt = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(self.salt)

    def generate_key(self, password):
        """Generate encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)

    def save_message(self, message, password):
        """Save encrypted message"""
        f = self.generate_key(password)
        messages = self.load_messages(password)
        
        messages.append({
            'content': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        encrypted_data = f.encrypt(json.dumps(messages).encode())
        with open(self.messages_file, 'wb') as file:
            file.write(encrypted_data)

    def load_messages(self, password):
        """Load and decrypt messages"""
        if not os.path.exists(self.messages_file):
            return []
            
        try:
            f = self.generate_key(password)
            with open(self.messages_file, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except:
            return []

def type_print(text, delay=0.03):
    """Print text with secretive typing effect"""
    for char in text:
        style = random.choice(['bold red', 'bold white'])
        console.print(char, end='', style=style)
        time.sleep(delay)
    print()

def create_message_panel(message, index):
    """Create a styled message panel"""
    text = Text()
    text.append(f"Whisper #{index}\n", style="bold red")
    text.append(f"{message['timestamp']}\n\n", style="dim")
    text.append(message['content'], style="bold white")
    
    return Panel(
        text,
        border_style="red",
        title="[bold red]Secret Whisper[/]",
        subtitle="[dim]Encrypted Message[/]"
    )

def display_messages(messages):
    """Display messages with encryption visualization"""
    if not messages:
        console.print(Panel("No whispers found in the void...",
                          style="dim red",
                          title="Secure Vault"))
        return
    
    for i, message in enumerate(messages, 1):
        console.print(create_message_panel(message, i))
        time.sleep(0.3)  # Dramatic pause between messages

def secure_input(prompt_text):
    """Get input with secure display"""
    return Prompt.ask(prompt_text, password=True)

def main():
    """Main program with secure interface"""
    import random  # For random styling
    
    whisper = SecretWhisper()
    console.clear()
    
    type_print("🤫 Welcome to SecretWhisper", delay=0.05)
    type_print("   Secure Communication Channel", delay=0.03)
    print()
    
    # Get master password
    master_password = secure_input("[bold red]Enter master password[/]")
    
    while True:
        try:
            console.print("\n[red]Secure Options:[/]")
            console.print("1. [white]Send Whisper[/]")
            console.print("2. [white]View Whispers[/]")
            console.print("3. [white]Exit[/]")
            
            choice = input("\nSelect operation (1-3): ").strip()
            
            if choice == '1':
                print("\nCompose your whisper (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                
                message = '\n'.join(lines)
                if message:
                    whisper.save_message(message, master_password)
                    
                    # Encryption visualization
                    type_print("\n🔒 Encrypting whisper", delay=0.05)
                    for _ in range(3):
                        console.print(".", style="bold red", end='')
                        time.sleep(0.3)
                    print()
                    type_print("✨ Whisper secured in quantum vault", delay=0.03)
                
            elif choice == '2':
                # Decryption visualization
                type_print("\n🔓 Accessing quantum vault", delay=0.05)
                for _ in range(3):
                    console.print(".", style="bold red", end='')
                    time.sleep(0.3)
                print("\n")
                
                messages = whisper.load_messages(master_password)
                display_messages(messages)
                input("\nPress Enter to seal the vault...")
                
            elif choice == '3':
                type_print("\n🔒 Sealing quantum vault...", delay=0.05)
                break
                
        except KeyboardInterrupt:
            print("\n")
            type_print("🔒 Emergency vault seal initiated...", delay=0.05)
            break

if __name__ == "__main__":
    main() 