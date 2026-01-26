import socket
import threading

heroes = []
hero_names = {}

def broadcast(message, sender):
    for hero in heroes:
        if hero != sender:
            try:
                hero.send(message)
            except:
                hero.close()
                heroes.remove(hero)

def handle_hero(hero):
    try:
        hero.send("Enter your Hero name: ".encode())
        name = hero.recv(1024).decode()
        hero_names[hero] = name
        welcome_msg = f"⚔️ {name} has entered the LANverse!"
        print(welcome_msg)
        broadcast(welcome_msg.encode(), hero)

        while True:
            msg = hero.recv(1024)
            if msg:
                full_msg = f"{name}: {msg.decode()}"
                print(full_msg)
                broadcast(full_msg.encode(), hero)
            else:
                break
    except:
        pass
    finally:
        print(f"💀 {hero_names[hero]} has left.")
        broadcast(f"💀 {hero_names[hero]} has left.".encode(), hero)
        heroes.remove(hero)
        hero.close()

def summon_heroes():
    while True:
        hero, addr = master.accept()
        heroes.append(hero)
        thread = threading.Thread(target=handle_hero, args=(hero,))
        thread.start()

master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master.bind(("0.0.0.0", 12345))
master.listen()
print("🧙‍♂️ Chat Master is waiting for LAN Warriors...")

summon_heroes()
