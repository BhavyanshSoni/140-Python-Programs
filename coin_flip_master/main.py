# Created by Bhavyansh Soni
# Coin Flip Master - Advanced coin flipping with statistics and games

import sys
import os
import time
import random
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.terminal_styles import *

class CoinFlipMaster:
    def __init__(self):
        self.running = True
        self.flip_history = []
        self.streak_record = {"heads": 0, "tails": 0}
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        
        # Coin designs
        self.coin_designs = {
            "classic": {
                "heads": [
                    "  ╭─────────╮  ",
                    " ╱           ╲ ",
                    "│    HEADS    │",
                    "│      👑      │",
                    "│  ●       ●  │",
                    " ╲           ╱ ",
                    "  ╰─────────╯  "
                ],
                "tails": [
                    "  ╭─────────╮  ",
                    " ╱           ╲ ",
                    "│    TAILS    │",
                    "│      🦅      │",
                    "│  ●       ●  │",
                    " ╲           ╱ ",
                    "  ╰─────────╯  "
                ]
            },
            "cyber": {
                "heads": [
                    "  ┌─────────┐  ",
                    " ╱ ◆ ◆ ◆ ◆ ◆ ╲ ",
                    "│   NEURAL   │",
                    "│     🤖     │",
                    "│ ▲ ▲ ▲ ▲ ▲ │",
                    " ╲ ◆ ◆ ◆ ◆ ◆ ╱ ",
                    "  └─────────┘  "
                ],
                "tails": [
                    "  ┌─────────┐  ",
                    " ╱ ▼ ▼ ▼ ▼ ▼ ╲ ",
                    "│   MATRIX   │",
                    "│     🔋     │",
                    "│ ● ● ● ● ● │",
                    " ╲ ▼ ▼ ▼ ▼ ▼ ╱ ",
                    "  └─────────┘  "
                ]
            }
        }
        
        self.current_design = "classic"
    
    def flip_coin_animation(self):
        """Animate coin flip"""
        flip_frames = [
            "│",
            "╱",
            "─",
            "╲",
            "│",
            "╱",
            "─",
            "╲"
        ]
        
        print("\nFlipping coin...")
        for _ in range(3):
            for frame in flip_frames:
                print(f"\r     {frame}     ", end="")
                time.sleep(0.1)
        
        result = random.choice(["heads", "tails"])
        
        # Show final result
        print("\r" + " " * 20)  # Clear line
        coin_art = self.coin_designs[self.current_design][result]
        
        for line in coin_art:
            print(f"{Colors.PRIMARY}{line}{Colors.RESET}")
        
        print()
        return result
    
    def single_flip(self):
        """Single coin flip"""
        clear_screen()
        print_banner("🪙 SINGLE COIN FLIP 🪙")
        print()
        
        result = self.flip_coin_animation()
        
        # Record the flip
        flip_data = {
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.flip_history.append(flip_data)
        
        # Check for streaks
        self.update_streaks()
        
        result_color = Colors.PRIMARY if result == "heads" else Colors.SECONDARY
        print(f"{result_color}Result: {result.upper()}!{Colors.RESET}")
        
        # Show some stats
        print()
        print(f"{Colors.ACCENT}Total Flips: {Colors.WHITE}{len(self.flip_history)}{Colors.RESET}")
        
        if len(self.flip_history) > 1:
            heads_count = sum(1 for flip in self.flip_history if flip["result"] == "heads")
            tails_count = len(self.flip_history) - heads_count
            
            print(f"{Colors.ACCENT}Heads: {Colors.WHITE}{heads_count} ({heads_count/len(self.flip_history)*100:.1f}%){Colors.RESET}")
            print(f"{Colors.ACCENT}Tails: {Colors.WHITE}{tails_count} ({tails_count/len(self.flip_history)*100:.1f}%){Colors.RESET}")
        
        press_enter_to_continue()
    
    def multiple_flips(self):
        """Multiple coin flips"""
        clear_screen()
        print_banner("🪙 MULTIPLE COIN FLIPS 🪙")
        print()
        
        try:
            num_flips = int(get_input("How many flips? (1-100): "))
            if num_flips < 1 or num_flips > 100:
                print_error("Please enter a number between 1 and 100!")
                time.sleep(1)
                return
        except ValueError:
            print_error("Invalid number!")
            time.sleep(1)
            return
        
        clear_screen()
        print_banner(f"🪙 FLIPPING {num_flips} COINS 🪙")
        print()
        
        results = []
        
        # Animate multiple flips
        for i in range(num_flips):
            progress = (i + 1) / num_flips * 100
            print(f"\rFlipping... {i+1}/{num_flips} ({progress:.1f}%)", end="")
            
            result = random.choice(["heads", "tails"])
            results.append(result)
            
            # Record the flip
            flip_data = {
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.flip_history.append(flip_data)
            
            time.sleep(0.1)
        
        print("\n")
        
        # Analyze results
        heads_count = results.count("heads")
        tails_count = results.count("tails")
        heads_percent = (heads_count / num_flips) * 100
        tails_percent = (tails_count / num_flips) * 100
        
        print_separator()
        print(f"{Colors.ACCENT}RESULTS:{Colors.RESET}")
        print()
        print(f"{Colors.PRIMARY}Heads: {heads_count} ({heads_percent:.1f}%){Colors.RESET}")
        print(f"{Colors.SECONDARY}Tails: {tails_count} ({tails_percent:.1f}%){Colors.RESET}")
        
        # Visual representation
        print()
        self.show_results_chart(heads_count, tails_count)
        
        # Find longest streaks
        print()
        self.analyze_streaks(results)
        
        press_enter_to_continue()
    
    def show_results_chart(self, heads_count, tails_count):
        """Show visual chart of results"""
        total = heads_count + tails_count
        if total == 0:
            return
        
        max_width = 40
        heads_width = int((heads_count / total) * max_width)
        tails_width = max_width - heads_width
        
        heads_bar = "█" * heads_width
        tails_bar = "█" * tails_width
        
        print("Visual Distribution:")
        print(f"{Colors.PRIMARY}{heads_bar}{Colors.SECONDARY}{tails_bar}{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'Heads':<{heads_width}}{Colors.SECONDARY}{'Tails':<{tails_width}}{Colors.RESET}")
    
    def analyze_streaks(self, results):
        """Analyze streaks in results"""
        if not results:
            return
        
        longest_heads = 0
        longest_tails = 0
        current_heads = 0
        current_tails = 0
        
        for result in results:
            if result == "heads":
                current_heads += 1
                current_tails = 0
                longest_heads = max(longest_heads, current_heads)
            else:
                current_tails += 1
                current_heads = 0
                longest_tails = max(longest_tails, current_tails)
        
        print("Streak Analysis:")
        print(f"{Colors.PRIMARY}Longest Heads Streak: {longest_heads}{Colors.RESET}")
        print(f"{Colors.SECONDARY}Longest Tails Streak: {longest_tails}{Colors.RESET}")
    
    def prediction_game(self):
        """Coin flip prediction game"""
        clear_screen()
        print_banner("🔮 PREDICTION GAME 🔮")
        print()
        
        slow_print("Predict the outcome of coin flips!", 0.02, Colors.ACCENT)
        print()
        
        rounds = 10
        score = 0
        
        for round_num in range(1, rounds + 1):
            clear_screen()
            print_banner(f"🔮 ROUND {round_num}/{rounds} 🔮")
            print()
            
            print(f"Score: {score}/{round_num-1}")
            print()
            
            print("Predict the next flip:")
            print_menu_item(1, "Heads 👑")
            print_menu_item(2, "Tails 🦅")
            
            print()
            prediction = get_input("Your prediction (1-2): ")
            
            if prediction == "1":
                predicted = "heads"
                predicted_display = "Heads 👑"
            elif prediction == "2":
                predicted = "tails"
                predicted_display = "Tails 🦅"
            else:
                print_error("Invalid prediction! Skipping round...")
                time.sleep(1)
                continue
            
            print()
            print(f"You predicted: {predicted_display}")
            print()
            
            # Flip the coin
            result = self.flip_coin_animation()
            
            # Record the flip
            flip_data = {
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.flip_history.append(flip_data)
            
            if predicted == result:
                score += 1
                print_success("🎉 Correct prediction!")
            else:
                print_error("❌ Wrong prediction!")
            
            time.sleep(1.5)
        
        # Final score
        clear_screen()
        print_banner("🔮 PREDICTION GAME RESULTS 🔮")
        print()
        
        percentage = (score / rounds) * 100
        print(f"{Colors.ACCENT}Final Score: {Colors.PRIMARY}{score}/{rounds} ({percentage:.1f}%){Colors.RESET}")
        
        if percentage >= 80:
            rating = "🔮 PSYCHIC MASTER!"
            color = Colors.PRIMARY
        elif percentage >= 60:
            rating = "🎯 GOOD GUESSER!"
            color = Colors.WARNING
        elif percentage >= 40:
            rating = "🤔 AVERAGE PREDICTOR"
            color = Colors.SECONDARY
        else:
            rating = "🎲 PURE LUCK!"
            color = Colors.GRAY
        
        print(f"{Colors.ACCENT}Rating: {color}{rating}{Colors.RESET}")
        
        self.games_played += 1
        if percentage >= 50:
            self.wins += 1
        else:
            self.losses += 1
        
        press_enter_to_continue()
    
    def streak_challenge(self):
        """Try to get the longest streak"""
        clear_screen()
        print_banner("🔥 STREAK CHALLENGE 🔥")
        print()
        
        slow_print("Try to get the longest possible streak!", 0.02, Colors.ACCENT)
        print()
        
        print("Choose your target:")
        print_menu_item(1, "Heads Streak 👑")
        print_menu_item(2, "Tails Streak 🦅")
        
        print()
        choice = get_input("Your choice (1-2): ")
        
        if choice == "1":
            target = "heads"
            target_display = "Heads 👑"
        elif choice == "2":
            target = "tails"
            target_display = "Tails 🦅"
        else:
            print_error("Invalid choice!")
            time.sleep(1)
            return
        
        clear_screen()
        print_banner(f"🔥 {target_display.upper()} STREAK CHALLENGE 🔥")
        print()
        
        streak = 0
        max_streak = 0
        
        while True:
            print(f"Current Streak: {Colors.PRIMARY}{streak}{Colors.RESET}")
            print(f"Best Streak: {Colors.WARNING}{max_streak}{Colors.RESET}")
            print()
            
            choice = get_input("Press Enter to flip (or 'q' to quit): ")
            if choice.lower() == 'q':
                break
            
            result = self.flip_coin_animation()
            
            # Record the flip
            flip_data = {
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.flip_history.append(flip_data)
            
            if result == target:
                streak += 1
                max_streak = max(max_streak, streak)
                print_success(f"🔥 Streak continues! {streak} in a row!")
            else:
                if streak > 0:
                    print_error(f"💔 Streak broken at {streak}!")
                else:
                    print_info("Keep trying for that first streak!")
                streak = 0
            
            print()
            time.sleep(1)
            clear_screen()
            print_banner(f"🔥 {target_display.upper()} STREAK CHALLENGE 🔥")
            print()
        
        # Update records
        if max_streak > self.streak_record[target]:
            self.streak_record[target] = max_streak
            print_success(f"🏆 NEW RECORD! {target.title()} streak: {max_streak}")
        
        print(f"Final best streak: {max_streak}")
        press_enter_to_continue()
    
    def statistics_dashboard(self):
        """Show detailed statistics"""
        clear_screen()
        print_banner("📊 STATISTICS DASHBOARD 📊")
        print()
        
        if not self.flip_history:
            print_warning("No flip data available!")
            print_info("Flip some coins to see statistics!")
            press_enter_to_continue()
            return
        
        total_flips = len(self.flip_history)
        heads_count = sum(1 for flip in self.flip_history if flip["result"] == "heads")
        tails_count = total_flips - heads_count
        
        # Basic statistics
        slow_print(f"Total Flips: {total_flips}", 0.02, Colors.ACCENT)
        slow_print(f"Heads: {heads_count} ({heads_count/total_flips*100:.1f}%)", 0.02, Colors.PRIMARY)
        slow_print(f"Tails: {tails_count} ({tails_count/total_flips*100:.1f}%)", 0.02, Colors.SECONDARY)
        
        print()
        slow_print("Game Statistics:", 0.02, Colors.ACCENT)
        slow_print(f"Games Played: {self.games_played}", 0.02, Colors.WHITE)
        if self.games_played > 0:
            win_rate = (self.wins / self.games_played) * 100
            slow_print(f"Win Rate: {win_rate:.1f}%", 0.02, Colors.WHITE)
        
        print()
        slow_print("Streak Records:", 0.02, Colors.ACCENT)
        slow_print(f"Best Heads Streak: {self.streak_record['heads']}", 0.02, Colors.PRIMARY)
        slow_print(f"Best Tails Streak: {self.streak_record['tails']}", 0.02, Colors.SECONDARY)
        
        # Recent activity
        print()
        slow_print("Recent Flips:", 0.02, Colors.ACCENT)
        recent_flips = self.flip_history[-10:]  # Last 10 flips
        recent_string = ""
        for flip in recent_flips:
            symbol = "H" if flip["result"] == "heads" else "T"
            color = Colors.PRIMARY if flip["result"] == "heads" else Colors.SECONDARY
            recent_string += f"{color}{symbol}{Colors.RESET} "
        
        print(recent_string)
        
        # Bias analysis
        print()
        if total_flips >= 10:
            expected = total_flips / 2
            heads_bias = abs(heads_count - expected)
            bias_percentage = (heads_bias / expected) * 100
            
            slow_print("Bias Analysis:", 0.02, Colors.ACCENT)
            if bias_percentage < 10:
                bias_result = "Fairly balanced"
                bias_color = Colors.PRIMARY
            elif bias_percentage < 20:
                bias_result = "Slight bias"
                bias_color = Colors.WARNING
            else:
                bias_result = "Noticeable bias"
                bias_color = Colors.ERROR
            
            print(f"{bias_color}{bias_result} ({bias_percentage:.1f}% deviation){Colors.RESET}")
        
        press_enter_to_continue()
    
    def coin_settings(self):
        """Coin design and settings"""
        clear_screen()
        print_banner("⚙️ COIN SETTINGS ⚙️")
        print()
        
        print("Available coin designs:")
        designs = list(self.coin_designs.keys())
        for i, design in enumerate(designs, 1):
            current = " (Current)" if design == self.current_design else ""
            print_menu_item(i, f"{design.title()}{current}")
        
        print()
        print_menu_item(len(designs) + 1, "Preview Designs")
        print_menu_item(len(designs) + 2, "Reset Statistics")
        print_menu_item(len(designs) + 3, "Back to Main Menu")
        
        print()
        choice = get_input(f"Select option (1-{len(designs) + 3}): ")
        
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(designs):
                self.current_design = designs[choice_num - 1]
                print_success(f"Coin design changed to {self.current_design}!")
            elif choice_num == len(designs) + 1:
                self.preview_designs()
            elif choice_num == len(designs) + 2:
                self.reset_statistics()
            elif choice_num == len(designs) + 3:
                return
        else:
            print_error("Invalid choice!")
        
        time.sleep(1)
    
    def preview_designs(self):
        """Preview all coin designs"""
        for design_name, design in self.coin_designs.items():
            clear_screen()
            print_banner(f"🪙 {design_name.upper()} DESIGN 🪙")
            print()
            
            print(f"{Colors.ACCENT}HEADS:{Colors.RESET}")
            for line in design["heads"]:
                print(f"{Colors.PRIMARY}{line}{Colors.RESET}")
            
            print()
            print(f"{Colors.ACCENT}TAILS:{Colors.RESET}")
            for line in design["tails"]:
                print(f"{Colors.SECONDARY}{line}{Colors.RESET}")
            
            print()
            input("Press Enter to continue...")
    
    def reset_statistics(self):
        """Reset all statistics"""
        confirm = get_input("Are you sure you want to reset all statistics? (y/N): ").lower()
        if confirm == 'y':
            self.flip_history = []
            self.streak_record = {"heads": 0, "tails": 0}
            self.games_played = 0
            self.wins = 0
            self.losses = 0
            print_success("All statistics reset!")
        else:
            print_info("Reset cancelled.")
    
    def update_streaks(self):
        """Update streak records"""
        if len(self.flip_history) < 2:
            return
        
        # Check current streak
        current_result = self.flip_history[-1]["result"]
        streak_count = 1
        
        # Count backwards to find streak length
        for i in range(len(self.flip_history) - 2, -1, -1):
            if self.flip_history[i]["result"] == current_result:
                streak_count += 1
            else:
                break
        
        # Update record if necessary
        if streak_count > self.streak_record[current_result]:
            self.streak_record[current_result] = streak_count
    
    def main_menu(self):
        """Display main menu"""
        while self.running:
            clear_screen()
            
            # Coin flip ASCII art
            coin_art = """
     ██████╗ ██████╗ ██╗███╗   ██╗    ███████╗██╗     ██╗██████╗ 
    ██╔════╝██╔═══██╗██║████╗  ██║    ██╔════╝██║     ██║██╔══██╗
    ██║     ██║   ██║██║██╔██╗ ██║    █████╗  ██║     ██║██████╔╝
    ██║     ██║   ██║██║██║╚██╗██║    ██╔══╝  ██║     ██║██╔═══╝ 
    ╚██████╗╚██████╔╝██║██║ ╚████║    ██║     ███████╗██║██║     
     ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝    ╚═╝     ╚══════╝╚═╝╚═╝     
            """
            
            print_ascii_art(coin_art, Colors.ACCENT)
            print()
            slow_print("Master the art of probability in cyberspace!", 0.02, Colors.PRIMARY)
            print()
            
            print_menu_item(1, "🪙 Single Flip")
            print_menu_item(2, "🪙 Multiple Flips")
            print_menu_item(3, "🔮 Prediction Game")
            print_menu_item(4, "🔥 Streak Challenge")
            print_menu_item(5, "📊 Statistics")
            print_menu_item(6, "⚙️ Settings")
            print_menu_item(7, "❌ Exit")
            
            print()
            if self.flip_history:
                last_flip = self.flip_history[-1]["result"]
                last_color = Colors.PRIMARY if last_flip == "heads" else Colors.SECONDARY
                print(f"{Colors.GRAY}Last flip: {last_color}{last_flip.title()}{Colors.RESET}")
            print()
            
            choice = get_input("Enter your choice (1-7): ")
            
            if choice == '1':
                self.single_flip()
            elif choice == '2':
                self.multiple_flips()
            elif choice == '3':
                self.prediction_game()
            elif choice == '4':
                self.streak_challenge()
            elif choice == '5':
                self.statistics_dashboard()
            elif choice == '6':
                self.coin_settings()
            elif choice == '7':
                slow_print("May probability be ever in your favor! 🪙", 0.02, Colors.SECONDARY)
                self.running = False
            else:
                print_error("Invalid choice! Please select 1-7.")
                time.sleep(1)

def main():
    """Main function to run Coin Flip Master"""
    try:
        coin_master = CoinFlipMaster()
        coin_master.main_menu()
    except KeyboardInterrupt:
        print()
        slow_print("Program interrupted by user.", 0.02, Colors.WARNING)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
