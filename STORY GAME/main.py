import random
import time

class Player:
    def __init__(self):
        answers = [
            "a keyboard",
            "a candle",
            "a secret"
        ]

        questions = [
            "which thing has keys but no locks, space but you can't fit and enter but you can't go in?",
            "I am young when i am tall but i am old when i am short. Who am i?",
            "Which thing brokes when you tell it?"
        ]

        options = [
            "a house", "a lock", "a keyboard",
            "a mountain", "a candle", "a building",
            "a secret", "a promise", "a glass"
        ]
        
        hp = 100
        food = 0
        weapon = 0
        attack_damage = 0
        monster_hp = 100
        monster_attack_damage = 30
        def Level_1():
            print(f"{questions[0]}\n")
            time.sleep(1)
            print(f"(a) {options[0]}\t(b) {options[1]}\t(c) {options[2]}")
            time.sleep(1)
            answer = input("Type the Answer: ")
            if answer.lower() == answers[0]:
                print("Wow! Correct Answer\n")
                time.sleep(1)
                print("Now You have 20 Bread which increase 5 health\n")
                food = 20
                time.sleep(1)
                print("A sword which deals 20 damage\n")
                weapon = 1
                attack_damage = 20

                print("Time for the First Monster ☠\n")
                time.sleep(2)
                print("Here It Comes ☠ !")

                while monster_hp == 100:
                    print("\nYour HP:", hp)
                    print("Monster HP:", monster_hp)
                    print("\n1. Attack")
                    print("2. Heal")
                    choice = input("What would you like to do? ")
                    
                    if choice == "1":
                        monster_hp -= attack_damage
                        print(f"\nYou dealt {attack_damage} damage!")
                    elif choice == "2" and food > 0:
                        hp += 5
                        food -= 1
                        print("\nYou healed 5 HP!")
                    else:
                        print("\nInvalid choice or no food left!")
                    
                    if monster_hp > 0:
                        hp -= monster_attack_damage
                        print(f"Monster dealt {monster_attack_damage} damage!")
                    
                    if hp <= 0:
                        print("\nGame Over! You died!")
                        break
                    elif monster_hp <= 0:
                        print("\nCongratulations! You defeated the monster!")
                        break
            else:
                print("Wrong Answer...")
                time.sleep(1)

        