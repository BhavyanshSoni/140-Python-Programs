import socket
import threading
import sys

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode()
            print(msg)
        except:
            print("⚠️ Connection to LANverse lost.")
            client.close()
            break

def send_messages():
    while True:
        msg = input()
        client.send(msg.encode())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(("127.0.0.1", 12345))  # Replace with server IP for LAN
except:
    print("❌ Could not connect to Chat Master.")
    sys.exit()

receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()
