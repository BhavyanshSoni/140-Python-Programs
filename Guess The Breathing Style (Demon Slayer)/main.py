from time import sleep
from random import choice

class Breathing:
    def __init__(self):
        self.breathing_styles = {
            "Tanjiro": "Hinokami Kagura",
            "Zenitsu": "Thunder Breathing",
            "Inosuke": "Beast Breathing",
            "Tengen": "Sound Breathing",
            "Gyomei": "Stone Breathing",
            "Muichiro": "Mist Breathing",
            "Mitsuri": "Love Breathing",
            "Obanai": "Serpent Breathing",
            "Kyojoro Rengoku": "Flame Breathing",
            "Tomiyoka": "Water Breathing",
            "Kokushibo": "Moon Breathing"
        }
    
    def s(self, txt, delay=0.04):
        for char in txt:
            print(char, end="", flush=True)
            sleep(delay)
        print()
    
    def welcome(self):
        self.s("In this game you have to guess a breathing style from the DEMON SLAYER series")
        self.s("You will be given a list of breathing styles and who use it you have to guess the correct one")
    
    def game(self):
        self.s("Let's Start the game")
        self.s("You will have 5 rounds to guess!")
        
        round_num = 1
        used_breathing_styles = []
        
        while round_num <= 5:
            self.s(f"\n--- Round {round_num}/5 ---")
            breathing_styles_list = list(self.breathing_styles.values())
            characters_list = list(self.breathing_styles.keys())
            
            # Get available breathing styles (not used yet)
            available_styles = [style for style in breathing_styles_list if style not in used_breathing_styles]
            random_breathing_style = choice(available_styles)
            used_breathing_styles.append(random_breathing_style)
            
            self.s(f"Who uses {random_breathing_style}?")
            answer = input("Enter your answer: ")
            
            # Find the correct character for this breathing style
            correct_character = None
            for character, style in self.breathing_styles.items():
                if style == random_breathing_style:
                    correct_character = character
                    break
            
            if answer.lower() == correct_character.lower():
                self.s("Correct!")
            else:
                self.s(f"Wrong! The correct answer is {correct_character}")
            
            round_num += 1
        
        self.s("\nGame Over! Thanks for playing!")

# Create instance and play the game
game_instance = Breathing()
game_instance.welcome()
game_instance.game()