import os
import sys
from colorama import Fore, Style, init
init(autoreset=True)

from modules import tasks, vault, games, file_tools, brain, voice_control

def print_logo():
    print(Fore.MAGENTA + Style.BRIGHT + r"""
  ██████╗  ██████╗ ██████╗      █████╗ ██╗     
 ██╔════╝ ██╔═══██╗██╔══██╗    ██╔══██╗██║     
 ██║  ███╗██║   ██║██████╔╝    ███████║██║     
 ██║   ██║██║   ██║██╔═══╝     ██╔══██║██║     
 ╚██████╔╝╚██████╔╝██║         ██║  ██║███████╗
  ╚═════╝  ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚══════╝
        GOD AI TERMINAL  v1.0 👁️‍🗨️       
""")

def help_menu():
    print(Fore.CYAN + "\n🔧 Commands:")
    print("  Help         Show this help menu")
    print("  Tasks        Open task manager")
    print("  Vault        Open secure vault")
    print("  Games        Open games hub")
    print("  Files        Use file tools")
    print("  Speak        Use voice control")
    print("  Exit         Close GOD AI\n")

def main():
    print_logo()
    help_menu()

    while True:
        cmd = input(Fore.YELLOW + "\n💻 > ").strip().lower()

        if cmd == "help":
            help_menu()
        elif cmd == "tasks":
            tasks.task_menu()
        elif cmd == "vault":
            vault.vault_menu()
        elif cmd == "games":
            games.launch_games()
        elif cmd == "files":
            file_tools.run_tools()
        elif cmd == "speak":
            voice_control.listen()
        elif cmd == "exit":
            print(Fore.RED + "Exiting... See you next time 👋")
            break
        else:
            brain.handle_command(cmd)

if __name__ == "__main__":
    main()