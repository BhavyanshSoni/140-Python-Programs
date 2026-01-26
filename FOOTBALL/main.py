import os
import random
import time

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except:
    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        CYAN = ''
        MAGENTA = ''
    class Style:
        BRIGHT = ''
        RESET_ALL = ''

EMOJI_BALL = "⚽"
EMOJI_GOAL = "🥅"
EMOJI_KICK = "🦵"
EMOJI_CHECK = "✅"
EMOJI_CROSS = "❌"
EMOJI_WHISTLE = "📯"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(text, sec=0.04):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(sec)
    print()

def football_game():
    clear()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}⚽ TERMINAL FOOTBALL GAME ⚽\n")
    print(f"{Fore.CYAN}Welcome to the match! {EMOJI_BALL}{EMOJI_GOAL}")
    time.sleep(1)

    position = 30  # Starting midfield (0=goal, 100=own goal)
    score = 0
    opponent_score = random.randint(0, 2)

    print(f"\n{Fore.YELLOW}Your opponent already has {opponent_score} goals.\n")

    while position > 0:
        print(f"\n{Fore.CYAN}Ball Position: {position} meters from goal 🥅")

        if position <= 10:
            print(f"\n{Fore.GREEN}You are very close to the goal! 🥅")
        
        chance = max(30, 100 - position)  # Closer you are, higher chance
        print(f"{Fore.YELLOW}Chance of goal if you shoot now: {chance}%")

        choice = input(f"\n{Fore.CYAN}Do you want to 'pass' or 'shoot'? ").lower()

        if choice == 'pass':
            success = random.choices([True, False], weights=[80, 20])[0]
            if success:
                move = random.randint(10, 30)
                position = max(position - move, 0)
                print(f"{Fore.GREEN}{EMOJI_CHECK} Successful pass! Ball moves {move} meters closer.")
            else:
                print(f"{Fore.RED}{EMOJI_CROSS} Bad pass! Opponent takes the ball!")
                print(f"\n{Fore.YELLOW}Opponent attacks... Shoots... ", end="")
                time.sleep(2)
                opp_goal = random.choice([True, False])
                if opp_goal:
                    opponent_score += 1
                    print(f"{Fore.RED}Goal for Opponent! 🥅")
                else:
                    print(f"{Fore.GREEN}Missed! You regain possession.")
                    position = 50
        elif choice == 'shoot':
            outcome = random.randint(1, 100)
            print(f"\n{Fore.CYAN}Player takes a shot... {EMOJI_KICK}")
            time.sleep(1)

            if outcome <= chance:
                print(f"{Fore.GREEN}GOOOAALLLLL!!!! {EMOJI_BALL}{EMOJI_GOAL}")
                score += 1
                break
            elif outcome <= chance + 10:
                print(f"{Fore.YELLOW}It's a CORNER kick! {EMOJI_WHISTLE}")
                corner_outcome = random.choice(['Goal', 'Miss', 'Opponent'])
                time.sleep(1)
                if corner_outcome == 'Goal':
                    print(f"{Fore.GREEN}Header... AND IT'S A GOAL! {EMOJI_GOAL}")
                    score += 1
                    break
                elif corner_outcome == 'Miss':
                    print(f"{Fore.RED}Missed the header... Ball goes out.")
                    break
                else:
                    print(f"{Fore.RED}Opponent clears the ball.")
                    position = 50
            elif outcome <= chance + 15:
                print(f"{Fore.YELLOW}PENALTY!! {EMOJI_WHISTLE}")
                pen = random.choice(['Goal', 'Miss'])
                time.sleep(1)
                if pen == 'Goal':
                    print(f"{Fore.GREEN}GOAL from the penalty spot! {EMOJI_GOAL}")
                    score += 1
                    break
                else:
                    print(f"{Fore.RED}Missed the penalty... Keeper saves it!")
                    break
            elif outcome <= chance + 25:
                print(f"{Fore.RED}Ball goes OUTSIDE! {EMOJI_CROSS}")
                break
            else:
                print(f"{Fore.RED}Saved by the goalkeeper! {EMOJI_CROSS}")
                break
        else:
            print(f"{Fore.RED}Invalid choice. You lose the ball!")
            position = 50

    print("\n" + "-"*40)
    print(f"\n{Fore.CYAN}Final Score:")
    print(f"{Fore.GREEN}You: {score}")
    print(f"{Fore.RED}Opponent: {opponent_score}")

    if score > opponent_score:
        print(f"\n{Fore.GREEN}🎉 YOU WIN THE MATCH! 🏆")
    elif score < opponent_score:
        print(f"\n{Fore.RED}😢 You Lost the Match.")
    else:
        print(f"\n{Fore.YELLOW}🤝 Match Drawn!")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    football_game()
