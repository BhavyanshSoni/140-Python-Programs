import time
import json
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress
from datetime import datetime, timedelta
import random

# Initialize Rich console
console = Console()

# Time travel themed elements
TIME_SYMBOLS = '⌛ 🕰️ ⚡ 🌀 ✨'
TIME_PERIODS = {
    "past": {
        "color": "blue",
        "emoji": "⌛",
        "description": "Messages to your past self"
    },
    "present": {
        "color": "green",
        "emoji": "⚡",
        "description": "Notes for the current timeline"
    },
    "future": {
        "color": "magenta",
        "emoji": "🌀",
        "description": "Letters to your future self"
    },
    "paradox": {
        "color": "red",
        "emoji": "✨",
        "description": "Temporal anomalies and random thoughts"
    }
}

class TimeSlipNote:
    def __init__(self):
        self.notes_file = "timeslip_notes.json"
        self.notes = self.load_notes()

    def load_notes(self):
        """Load notes from the time stream"""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_notes(self):
        """Save notes to the time stream"""
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=2)

    def add_note(self, content, time_period, future_date=None):
        """Add a new note to the time stream"""
        note = {
            'id': len(self.notes) + 1,
            'content': content,
            'time_period': time_period,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'future_date': future_date
        }
        self.notes.append(note)
        self.save_notes()
        return note

    def get_notes_by_period(self, time_period):
        """Get notes from a specific time period"""
        return [note for note in self.notes if note['time_period'] == time_period]

    def get_future_notes_due(self):
        """Get future notes that are due to be read"""
        current_date = datetime.now()
        due_notes = []
        
        for note in self.notes:
            if note['time_period'] == 'future' and note['future_date']:
                future_date = datetime.strptime(note['future_date'], "%Y-%m-%d")
                if current_date.date() >= future_date.date():
                    due_notes.append(note)
        
        return due_notes

def type_print(text, delay=0.03):
    """Print text with time travel effect"""
    for char in text:
        style = random.choice(['bold cyan', 'bold blue', 'bold magenta'])
        console.print(char, end='', style=style)
        time.sleep(delay)
    print()

def create_note_panel(note):
    """Create a time-themed note panel"""
    period_info = TIME_PERIODS[note['time_period']]
    
    text = Text()
    text.append(f"{period_info['emoji']} ", style=period_info['color'])
    text.append(note['content'] + "\n\n", style="bold white")
    
    if note['future_date']:
        text.append("Temporal Destination: ", style="dim")
        text.append(note['future_date'], style="cyan")
    
    return Panel(
        text,
        title=f"[{period_info['color']}]Time Note #{note['id']}[/]",
        subtitle=f"[dim]Created: {note['created']}[/]",
        border_style=period_info['color']
    )

def display_time_periods():
    """Display available time periods"""
    table = Table(title="[bold]Temporal Destinations[/]")
    table.add_column("Period", style="cyan")
    table.add_column("Description", style="white")
    
    for period, info in TIME_PERIODS.items():
        table.add_row(
            f"{info['emoji']} {period.title()}",
            info['description']
        )
    
    console.print(table)

def simulate_time_travel():
    """Create a time travel animation effect"""
    symbols = list('⌛🕰️⚡🌀✨')
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Initiating temporal shift...[/]", total=100)
        
        while not progress.finished:
            for symbol in symbols:
                console.print(f"\r{symbol}", end='')
                progress.update(task, advance=5)
                time.sleep(0.1)
    print()

def display_notes(notes):
    """Display notes with time travel effects"""
    if not notes:
        console.print(Panel("No notes found in this timeline...",
                          style="dim cyan",
                          title="Time Stream"))
        return
    
    for note in notes:
        console.print(create_note_panel(note))
        time.sleep(0.3)  # Temporal pause between notes

def main():
    """Main program with time travel interface"""
    timeslip = TimeSlipNote()
    console.clear()
    
    type_print("⌛ Welcome to TimeSlipNote", delay=0.05)
    type_print("   Write Across Time and Space", delay=0.03)
    print()
    
    # Check for due future notes
    due_notes = timeslip.get_future_notes_due()
    if due_notes:
        type_print("\n🌀 Messages from your past self have arrived!", delay=0.03)
        display_notes(due_notes)
        input("\nPress Enter to continue...")
    
    while True:
        try:
            console.print("\n[bold cyan]Temporal Operations:[/]")
            console.print("1. [white]Write New Note[/]")
            console.print("2. [white]View Time Stream[/]")
            console.print("3. [white]View Future Messages[/]")
            console.print("4. [white]Exit[/]")
            
            choice = input("\nSelect operation (1-4): ").strip()
            
            if choice == '1':
                console.clear()
                display_time_periods()
                time_period = input("\nEnter temporal destination: ").lower()
                
                if time_period not in TIME_PERIODS:
                    console.print("[red]Invalid time period.[/]")
                    continue
                
                print("\nWrite your message (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                
                content = '\n'.join(lines)
                future_date = None
                
                if time_period == 'future':
                    future_date = input("\nEnter future date (YYYY-MM-DD): ").strip()
                    try:
                        datetime.strptime(future_date, "%Y-%m-%d")
                    except:
                        console.print("[red]Invalid date format.[/]")
                        continue
                
                if content:
                    simulate_time_travel()
                    note = timeslip.add_note(content, time_period, future_date)
                    console.print(create_note_panel(note))
                    type_print("\n⚡ Note has been sent through the time stream!", delay=0.03)
                
            elif choice == '2':
                console.clear()
                display_time_periods()
                time_period = input("\nEnter time period to view (or 'all'): ").lower()
                
                if time_period == 'all':
                    notes = timeslip.notes
                elif time_period in TIME_PERIODS:
                    notes = timeslip.get_notes_by_period(time_period)
                else:
                    console.print("[red]Invalid time period.[/]")
                    continue
                
                console.clear()
                type_print(f"⌛ Viewing {time_period.title()} Timeline", delay=0.03)
                print()
                display_notes(notes)
                input("\nPress Enter to return to the present...")
                
            elif choice == '3':
                console.clear()
                type_print("🌀 Scanning Future Messages", delay=0.03)
                print()
                future_notes = timeslip.get_notes_by_period('future')
                display_notes(future_notes)
                input("\nPress Enter to return to the present...")
                
            elif choice == '4':
                type_print("\n⌛ Closing temporal gateway...", delay=0.05)
                break
                
        except KeyboardInterrupt:
            print("\n")
            type_print("⌛ Emergency temporal exit...", delay=0.05)
            break

if __name__ == "__main__":
    main() 