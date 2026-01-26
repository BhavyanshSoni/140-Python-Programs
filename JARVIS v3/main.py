#!/usr/bin/env python3
"""
🛠️ JARVISv3 - Advanced Utility Tool 💡
A powerful terminal-based utility for file management and system operations.
"""

import time
import random
import os
from pathlib import Path
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class JARVISv3Utility:
    """
    🛠️ Advanced JARVISv3 Utility Tool 💡
    
    A comprehensive utility system for file management,
    data processing, and system maintenance operations.
    """
    
    def __init__(self):
        """Initialize the utility with default settings."""
        self.operations_count = 0
        self.processed_files = []
        
    def slow_print(self, text: str, delay: float = 0.03, color: str = None):
        """Print text with typing animation effect."""
        if color:
            color_code = getattr(Fore, color.upper(), Fore.WHITE)
            text = f"{color_code}{text}{Style.RESET_ALL}"
        
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def display_banner(self):
        """Display the utility banner."""
        banner = f"""
    🛠️╔══════════════════════════════════════════════════════════════════════╗
    ║  ██    ██ ████████ ██ ██      ██ ████████ ██    ██                  ║
    ║  ██    ██    ██    ██ ██      ██    ██     ██  ██                   ║
    ║  ██    ██    ██    ██ ██      ██    ██      ████                    ║
    ║  ██    ██    ██    ██ ██      ██    ██       ██                     ║
    ║   ██████     ██    ██ ███████ ██    ██       ██                     ║
    ╚══════════════════════════════════════════════════════════════════════╝💡
    
                            JARVISv3 Utility Tool
                            Press ENTER to access tools...
        """
        
        print(banner)
    
    def scan_directory(self):
        """Scan current directory and show file information."""
        self.slow_print(f"\n🛠️ Scanning current directory...", color="CYAN")
        
        current_dir = Path.cwd()
        files = list(current_dir.iterdir())
        
        if not files:
            self.slow_print("Directory is empty.", color="YELLOW")
            return
        
        print(f"\nFound {len(files)} items in {current_dir.name}:")
        
        for item in files[:10]:  # Show first 10 items
            if item.is_file():
                size = item.stat().st_size
                size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                self.slow_print(f"  📄 {item.name} ({size_str})", delay=0.01)
            elif item.is_dir():
                self.slow_print(f"  📁 {item.name}/", delay=0.01)
        
        if len(files) > 10:
            self.slow_print(f"  ... and {len(files) - 10} more items", color="YELLOW")
    
    def file_organizer(self):
        """Simulate file organization operations."""
        self.slow_print(f"\n💡 Starting file organization...", color="MAGENTA")
        
        file_types = [
            ("Documents", ["txt", "doc", "pdf", "md"]),
            ("Images", ["jpg", "png", "gif", "bmp"]),
            ("Videos", ["mp4", "avi", "mov", "mkv"]),
            ("Audio", ["mp3", "wav", "flac", "ogg"]),
            ("Archives", ["zip", "tar", "gz", "rar"])
        ]
        
        for category, extensions in file_types:
            count = random.randint(0, 15)
            if count > 0:
                self.slow_print(f"  🛠️ Organizing {count} {category.lower()} files...", delay=0.02)
                time.sleep(0.8)
                self.slow_print(f"    ✅ {count} files moved to {category}/ folder", color="GREEN")
                self.processed_files.extend([f"file{i}.{extensions[0]}" for i in range(count)])
        
        self.operations_count += 1
    
    def system_cleanup(self):
        """Simulate system cleanup operations."""
        self.slow_print(f"\n💡 Performing system cleanup...", color="YELLOW")
        
        cleanup_tasks = [
            "Clearing temporary files",
            "Removing cache data",
            "Cleaning log files", 
            "Optimizing disk space",
            "Defragmenting storage"
        ]
        
        total_space_freed = 0
        
        for task in cleanup_tasks:
            self.slow_print(f"  🤖 {task}...", delay=0.02)
            time.sleep(random.uniform(0.5, 1.2))
            
            space_freed = random.randint(10, 500)
            total_space_freed += space_freed
            self.slow_print(f"    ✅ Freed {space_freed} MB", color="GREEN")
        
        self.slow_print(f"\n🛠️ Cleanup complete! Total space freed: {total_space_freed} MB", color="CYAN")
        self.operations_count += 1
    
    def data_processor(self):
        """Simulate data processing operations."""
        self.slow_print(f"\n💡 Starting data processing...", color="GREEN")
        
        data_types = ["CSV files", "JSON data", "XML documents", "Database records", "Log entries"]
        
        for data_type in data_types:
            records = random.randint(100, 10000)
            self.slow_print(f"  🛠️ Processing {records:,} {data_type.lower()}...", delay=0.02)
            time.sleep(1)
            
            processed = int(records * random.uniform(0.85, 0.98))
            errors = records - processed
            
            self.slow_print(f"    ✅ Processed: {processed:,}", color="GREEN")
            if errors > 0:
                self.slow_print(f"    ⚠️  Errors: {errors}", color="YELLOW")
        
        self.operations_count += 1
    
    def backup_creator(self):
        """Simulate backup creation process."""
        self.slow_print(f"\n💡 Creating system backup...", color="MAGENTA")
        
        backup_steps = [
            "Scanning files for backup",
            "Compressing data",
            "Encrypting backup",
            "Verifying integrity",
            "Finalizing backup"
        ]
        
        total_files = random.randint(500, 5000)
        
        for i, step in enumerate(backup_steps, 1):
            self.slow_print(f"  🤖 Step {i}/{len(backup_steps)}: {step}...", delay=0.02)
            time.sleep(random.uniform(1, 2))
            
            progress = int((i / len(backup_steps)) * 100)
            self.slow_print(f"    Progress: {progress}%", color="CYAN")
        
        backup_size = random.randint(100, 2000)
        self.slow_print(f"\n🛠️ Backup complete! {total_files:,} files backed up ({backup_size} MB)", color="GREEN")
        self.operations_count += 1
    
    def display_stats(self):
        """Display utility usage statistics."""
        print(f"\n💡 Utility Session Statistics:")
        print(f"  Operations performed: {self.operations_count}")
        print(f"  Files processed: {len(self.processed_files)}")
        print(f"  Session time: {time.strftime('%H:%M:%S')}")
    
    def interactive_menu(self):
        """Display interactive utility menu."""
        while True:
            print("\n" + "="*60)
            self.slow_print(f"\n🛠️ {folder_name} Utility - Main Menu", color="CYAN")
            self.slow_print(f"  1. 💡 Scan Directory")
            self.slow_print(f"  2. 🛠️ File Organizer")
            self.slow_print(f"  3. 💡 System Cleanup")
            self.slow_print(f"  4. 🤖 Data Processor")
            self.slow_print(f"  5. 🛠️ Backup Creator")
            self.slow_print(f"  6. 💡 View Statistics")
            self.slow_print(f"  7. 🛠️ Exit Utility")
            
            try:
                choice = input(f"\nSelect utility option (1-7): ")
                
                if choice == "1":
                    self.scan_directory()
                elif choice == "2":
                    self.file_organizer()
                elif choice == "3":
                    self.system_cleanup()
                elif choice == "4":
                    self.data_processor()
                elif choice == "5":
                    self.backup_creator()
                elif choice == "6":
                    self.display_stats()
                elif choice == "7":
                    self.shutdown_utility()
                    break
                else:
                    self.slow_print("❌ Invalid choice. Please try again.", color="RED")
                    
            except KeyboardInterrupt:
                self.shutdown_utility()
                break
    
    def shutdown_utility(self):
        """Gracefully shutdown the utility."""
        self.slow_print(f"💡 Shutting down {folder_name} Utility...", color="YELLOW")
        time.sleep(1)
        self.slow_print(f"\n🛠️ Utility session complete. All tools safely closed! 💡", color="GREEN")

def main():
    """Main entry point for the {folder_name} Utility."""
    utility = JARVISv3Utility()
    
    try:
        utility.display_banner()
        input()  # Wait for user to press ENTER
        utility.interactive_menu()
        
    except KeyboardInterrupt:
        utility.shutdown_utility()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
