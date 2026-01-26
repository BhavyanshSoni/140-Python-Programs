#!/usr/bin/env python3
"""
AI Comic Bot - Advanced Comic Story Generator
An intelligent comic book creation system with AI-powered storytelling and ASCII art generation.

Features:
- AI-powered story generation
- Character development and dialogue
- ASCII art comic panels
- Multiple comic genres and styles
- Interactive story branching
- Comic book formatting and layout
"""

import sys
import time
import os
import random
from typing import List, Dict, Tuple

class Colors:
    """ANSI color codes for terminal styling"""
    RESET = '\033'
    BOLD = '\033[1m'
    RED = '\033❌'
    GREEN = '\033✅'
    YELLOW = '\033⚠️'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    DIM = '\033[2m'

class Character:
    """Represents a comic book character"""
    def __init__(self, name: str, personality: str, powers: List[str] = None):
        self.name = name
        self.personality = personality
        self.powers = powers or []
        self.dialogue_style = self.generate_dialogue_style()
        
    def generate_dialogue_style(self):
        """Generate character-specific dialogue patterns"""
        styles = {
            'heroic': ['Justice will prevail!', 'I must protect the innocent!', 'Evil shall not triumph!'],
            'villain': ['Mwahahaha!', 'You fools!', 'My plan is perfect!'],
            'comic_relief': ['Oops!', 'Did I do that?', 'Well, this is awkward...'],
            'mysterious': ['...', 'Perhaps...', 'The truth is hidden...'],
            'tough': ['Bring it on!', 'Is that all you got?', 'Time to rumble!']
        }
        return styles.get(self.personality, ['Hello there!'])
        
    def speak(self):
        """Generate character dialogue"""
        return random.choice(self.dialogue_style)

class ComicPanel:
    """Represents a single comic panel"""
    def __init__(self, scene_description: str, characters: List[Character], dialogue: Dict[str, str]):
        self.scene_description = scene_description
        self.characters = characters
        self.dialogue = dialogue
        self.ascii_art = self.generate_ascii_scene()
        
    def generate_ascii_scene(self):
        """Generate ASCII art for the scene"""
        scenes = {
            'city': [
                "    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄",
                "   ██▀▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██",
                "   ██▀░░░░░░░░░░░░░░░░░░▀██",
                "   ██▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██",
                "      ████    ████    ████",
                "      ████    ████    ████"
            ],
            'battle': [
                "     ⚡ BOOM! ⚡",
                "   ▄████▄  💥  ▄████▄",
                "  ███  ███ WHAM! ███  ███",
                "   ▀████▀  POW!  ▀████▀",
                "     ⭐ CRASH! ⭐",
                "    💥 KAPOW! 💥"
            ],
            'laboratory': [
                "  ╔════════════════════╗",
                "  ║ [⚗️]  [🧪]  [⚛️] ║",
                "  ║                    ║",
                "  ║ ┌─────┐ ┌─────┐   ║",
                "  ║ │ ◉ ◉ │ │ ≋≋≋ │   ║",
                "  ║ └─────┘ └─────┘   ║",
                "  ╚════════════════════╝"
            ],
            'space': [
                "    🌟  ✦    🌟     ✦",
                "  ✦     🌟  ✦   🌟",
                "     🌟    ✦     🌟  ✦",
                "  ✦   🚀       ✦    🌟",
                "    🌟  ✦  🌍  ✦  🌟",
                "  ✦     🌟    ✦     ✦"
            ]
        }
        
        # Determine scene type based on description
        scene_type = 'city'  # default
        if any(word in self.scene_description.lower() for word in ['fight', 'battle', 'combat']):
            scene_type = 'battle'
        elif any(word in self.scene_description.lower() for word in ['lab', 'science', 'experiment']):
            scene_type = 'laboratory'
        elif any(word in self.scene_description.lower() for word in ['space', 'star', 'planet']):
            scene_type = 'space'
            
        return scenes.get(scene_type, scenes['city'])

class ComicStory:
    """Manages the overall comic story"""
    def __init__(self, genre: str = 'superhero'):
        self.genre = genre
        self.title = ""
        self.panels = []
        self.characters = []
        self.story_arc = []
        
    def generate_characters(self):
        """Generate characters based on genre"""
        character_templates = {
            'superhero': [
                Character("Captain Thunder", "heroic", ["lightning", "flight"]),
                Character("Dr. Doom", "villain", ["genius intellect", "armor"]),
                Character("Sidekick Sam", "comic_relief", ["enthusiasm"])
            ],
            'sci-fi': [
                Character("Commander Nova", "tough", ["plasma cannon", "jetpack"]),
                Character("Alien Overlord", "mysterious", ["telepathy", "shapeshifting"]),
                Character("Robot R2", "comic_relief", ["repairs", "scanning"])
            ],
            'fantasy': [
                Character("Wizard Merlin", "mysterious", ["magic", "wisdom"]),
                Character("Dark Lord", "villain", ["dark magic", "undead army"]),
                Character("Brave Knight", "heroic", ["sword", "courage"])
            ]
        }
        
        self.characters = character_templates.get(self.genre, character_templates['superhero'])
        
    def generate_story_arc(self):
        """Generate a complete story arc"""
        story_templates = {
            'superhero': [
                "The city is in danger from a new villain",
                "Our hero discovers the villain's evil plan",
                "An epic battle ensues in the city center",
                "The hero faces their greatest challenge",
                "Good triumphs over evil, the city is saved"
            ],
            'sci-fi': [
                "Alien ships appear in Earth's atmosphere",
                "First contact goes terribly wrong",
                "Humanity must defend against invasion",
                "A secret weapon is discovered",
                "Peace is restored through understanding"
            ],
            'fantasy': [
                "An ancient evil awakens from slumber",
                "The chosen hero begins their quest",
                "Magical allies join the journey",
                "The final confrontation approaches",
                "Light conquers darkness once again"
            ]
        }
        
        self.story_arc = story_templates.get(self.genre, story_templates['superhero'])
        self.title = f"The Amazing Adventures of {self.characters[0].name}"
        
    def create_panel(self, scene_idx: int):
        """Create a comic panel for a specific scene"""
        if scene_idx >= len(self.story_arc):
            return None
            
        scene_description = self.story_arc[scene_idx]
        
        # Select characters for this scene
        scene_characters = random.sample(self.characters, min(2, len(self.characters)))
        
        # Generate dialogue
        dialogue = {}
        for char in scene_characters:
            dialogue[char.name] = char.speak()
            
        panel = ComicPanel(scene_description, scene_characters, dialogue)
        return panel

class ComicBot:
    """Main AI Comic Bot system"""
    def __init__(self):
        self.current_story = None
        self.reading_mode = False
        
    def display_banner(self):
        """Display AI Comic Bot banner"""
        banner = [
            "╔══════════════════════════════════════╗",
            "║           AI COMIC BOT               ║",
            "║     Intelligent Story Generator      ║",
            "╚══════════════════════════════════════╝"
        ]
        
        print("\n")
        for line in banner:
            print(f"{Colors.BRIGHT_MAGENTA}{line}{Colors.RESET}")
        print("\n")
        
    def draw_panel(self, panel: ComicPanel, panel_number: int):
        """Draw a comic panel with ASCII art and dialogue"""
        # Panel border
        print(f"{Colors.BRIGHT_CYAN}╔{'═' * 50}╗{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}║{Colors.BRIGHT_YELLOW} Panel {panel_number}: {panel.scene_description:<40} {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}╠{'═' * 50}╣{Colors.RESET}")
        
        # ASCII art scene
        for line in panel.ascii_art:
            print(f"{Colors.BRIGHT_CYAN}║{Colors.BRIGHT_WHITE}{line:^48}{Colors.BRIGHT_CYAN}║{Colors.RESET}")
            
        # Character dialogue
        print(f"{Colors.BRIGHT_CYAN}╠{'═' * 50}╣{Colors.RESET}")
        for char_name, dialogue in panel.dialogue.items():
            # Character name in speech bubble style
            print(f"{Colors.BRIGHT_CYAN}║ {Colors.BRIGHT_GREEN}{char_name}:{Colors.WHITE} \"{dialogue}\"" + " " * (45 - len(char_name) - len(dialogue)) + f"{Colors.BRIGHT_CYAN}║{Colors.RESET}")
            
        print(f"{Colors.BRIGHT_CYAN}╚{'═' * 50}╝{Colors.RESET}")
        print()
        
    def create_comic(self, genre: str):
        """Create a complete comic story"""
        print(f"{Colors.BRIGHT_GREEN}Creating {genre} comic...{Colors.RESET}")
        time.sleep(1)
        
        self.current_story = ComicStory(genre)
        self.current_story.generate_characters()
        self.current_story.generate_story_arc()
        
        # Create panels for each story beat
        for i, scene in enumerate(self.current_story.story_arc):
            panel = self.current_story.create_panel(i)
            if panel:
                self.current_story.panels.append(panel)
                
        print(f"{Colors.BRIGHT_GREEN}Comic created successfully!{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}Title: {self.current_story.title}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Panels: {len(self.current_story.panels)}{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}Characters: {', '.join([c.name for c in self.current_story.characters])}{Colors.RESET}")
        
    def read_comic(self):
        """Display the comic in reading mode"""
        if not self.current_story:
            print(f"{Colors.BRIGHT_RED}No comic loaded! Create one first.{Colors.RESET}")
            return
            
        print(f"\n{Colors.BRIGHT_YELLOW}═══ {self.current_story.title} ═══{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Genre: {self.current_story.genre.title()}{Colors.RESET}\n")
        
        for i, panel in enumerate(self.current_story.panels):
            self.draw_panel(panel, i + 1)
            
            if i < len(self.current_story.panels) - 1:
                input(f"{Colors.BRIGHT_GREEN}Press Enter for next panel...{Colors.RESET}")
                
        print(f"\n{Colors.BRIGHT_YELLOW}═══ THE END ═══{Colors.RESET}")
        
    def interactive_story(self):
        """Create an interactive story with choices"""
        if not self.current_story:
            print(f"{Colors.BRIGHT_RED}No comic loaded! Create one first.{Colors.RESET}")
            return
            
        print(f"\n{Colors.BRIGHT_MAGENTA}🎮 Interactive Story Mode 🎮{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Make choices to influence the story!{Colors.RESET}\n")
        
        for i, panel in enumerate(self.current_story.panels):
            self.draw_panel(panel, i + 1)
            
            if i < len(self.current_story.panels) - 1:
                # Present choices
                print(f"{Colors.BRIGHT_YELLOW}What happens next?{Colors.RESET}")
                choices = [
                    "The hero uses their special power",
                    "A new character appears",
                    "An unexpected twist occurs"
                ]
                
                for j, choice in enumerate(choices, 1):
                    print(f"  {Colors.BRIGHT_GREEN}{j}{Colors.RESET}. {choice}")
                    
                try:
                    choice_num = int(input(f"\n{Colors.BRIGHT_CYAN}Choose (1-3): {Colors.RESET}"))
                    if 1 <= choice_num <= 3:
                        chosen_action = choices[choice_num - 1]
                        print(f"\n{Colors.BRIGHT_MAGENTA}You chose: {chosen_action}{Colors.RESET}")
                        
                        # Modify next panel based on choice
                        if i + 1 < len(self.current_story.panels):
                            next_panel = self.current_story.panels[i + 1]
                            next_panel.scene_description += f" ({chosen_action})"
                            
                except ValueError:
                    print(f"{Colors.BRIGHT_RED}Invalid choice, continuing with original story...{Colors.RESET}")
                    
                input(f"{Colors.BRIGHT_GREEN}Press Enter to continue...{Colors.RESET}")
                
        print(f"\n{Colors.BRIGHT_YELLOW}═══ YOUR STORY ENDS ═══{Colors.RESET}")

def slow_print(text, delay=0.03, color=Colors.BRIGHT_MAGENTA):
    """Print text with slow typing effect"""
    for char in text:
        sys.stdout.write(color + char + Colors.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    """Main application entry point"""
    try:
        bot = ComicBot()
        
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            bot.display_banner()
            
            slow_print("Welcome to AI Comic Bot!", delay=0.05)
            print()
            
            slow_print("Features:", color=Colors.BRIGHT_CYAN)
            features = [
                "AI-powered story generation",
                "Character development and dialogue",
                "ASCII art comic panels",
                "Multiple comic genres",
                "Interactive story choices",
                "Professional comic formatting"
            ]
            
            for i, feature in enumerate(features, 1):
                slow_print(f"  {i}. {feature}", delay=0.01, color=Colors.GREEN)
            print()
            
            print(f"{Colors.BRIGHT_CYAN}Choose an option:{Colors.RESET}")
            print(f"{Colors.GREEN}1 - Create Superhero Comic")
            print(f"{Colors.GREEN}2 - Create Sci-Fi Comic")
            print(f"{Colors.GREEN}3 - Create Fantasy Comic")
            print(f"{Colors.GREEN}4 - Read Current Comic")
            print(f"{Colors.GREEN}5 - Interactive Story Mode")
            print(f"{Colors.GREEN}6 - Character Gallery")
            print(f"{Colors.GREEN}q - Quit")
            
            choice = input(f"\n{Colors.BRIGHT_CYAN}Enter choice: {Colors.RESET}").strip().lower()
            
            if choice == '1':
                bot.create_comic('superhero')
                input(f"\n{Colors.BRIGHT_GREEN}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '2':
                bot.create_comic('sci-fi')
                input(f"\n{Colors.BRIGHT_GREEN}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '3':
                bot.create_comic('fantasy')
                input(f"\n{Colors.BRIGHT_GREEN}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '4':
                bot.read_comic()
                input(f"\n{Colors.BRIGHT_GREEN}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '5':
                bot.interactive_story()
                input(f"\n{Colors.BRIGHT_GREEN}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '6':
                if bot.current_story:
                    print(f"\n{Colors.BRIGHT_YELLOW}Character Gallery:{Colors.RESET}")
                    for char in bot.current_story.characters:
                        print(f"\n{Colors.BRIGHT_GREEN}🦸 {char.name}{Colors.RESET}")
                        print(f"  Personality: {char.personality}")
                        print(f"  Powers: {', '.join(char.powers) if char.powers else 'None'}")
                        print(f"  Catchphrase: \"{char.speak()}\"")
                else:
                    print(f"{Colors.BRIGHT_RED}No characters available. Create a comic first!{Colors.RESET}")
                input(f"\n{Colors.BRIGHT_GREEN}Press Enter to continue...{Colors.RESET}")
                
            elif choice == 'q':
                slow_print("Thanks for reading! Keep creating amazing stories!", color=Colors.BRIGHT_GREEN)
                break
                
            else:
                print(f"{Colors.BRIGHT_RED}Invalid choice!{Colors.RESET}")
                time.sleep(1)
                
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}Error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()