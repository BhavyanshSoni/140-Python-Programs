from time import sleep
from getpass import getpass
from datetime import datetime
import json
import os
import secrets
import hashlib


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DATA_DIR, "db.json")


def s(txt, delay=0.02):
	for c in txt:
		print(c, end='', flush=True)
		sleep(delay)
	print()


def ensure_store():
	if not os.path.isdir(DATA_DIR):
		os.makedirs(DATA_DIR, exist_ok=True)
	if not os.path.isfile(DB_PATH):
		with open(DB_PATH, "w", encoding="utf-8") as f:
			json.dump({"users": {}}, f, indent=2)


def load_db():
	ensure_store()
	with open(DB_PATH, "r", encoding="utf-8") as f:
		return json.load(f)


def save_db(db):
	with open(DB_PATH, "w", encoding="utf-8") as f:
		json.dump(db, f, indent=2)


def hash_password(password, salt_hex):
	return hashlib.sha256((salt_hex + password).encode("utf-8")).hexdigest()


def prompt_int(prompt, valid_set=None):
	while True:
		val = input(prompt).strip()
		if not val.isdigit():
			s("Please enter a number.")
			continue
		inum = int(val)
		if valid_set is not None and inum not in valid_set:
			s("Invalid choice. Try again.")
			continue
		return inum


def safe_getpass(prompt):
	try:
		return getpass(prompt)
	except Exception:
		# Some editors/terminals (esp. on Windows) don't support hidden input.
		s("(Password input not hidden in this console)")
		return input(prompt)


class Session:
	def __init__(self):
		ensure_store()
		s("Welcome to B-MAIL!\n")
		self.username = None

	def register(self):
		s("\nCreate your account")
		while True:
			username = input("Username>> ").strip().lower()
			if not username:
				s("Username cannot be empty.")
				continue
			db = load_db()
			if username in db["users"]:
				s("This username is taken. Choose another.")
				continue
			break
		while True:
			pwd1 = safe_getpass("Password>> ")
			pwd2 = safe_getpass("Confirm Password>> ")
			if pwd1 != pwd2:
				s("Passwords do not match. Try again.")
				continue
			if len(pwd1) < 4:
				s("Use at least 4 characters.")
				continue
			break
		salt = secrets.token_hex(16)
		pwd_hash = hash_password(pwd1, salt)
		db["users"][username] = {
			"email": f"{username}@bmail.com",
			"salt": salt,
			"password_hash": pwd_hash,
			"vault": [],
			"inbox": [],
			"sent": []
		}
		save_db(db)
		s("Account created successfully ✅\n")

	def login(self):
		s("\nLogin to your account")
		username = input("Username>> ").strip().lower()
		db = load_db()
		if username not in db["users"]:
			s("User not found.")
			return False
		pwd = safe_getpass("Password>> ")
		salt = db["users"][username]["salt"]
		if hash_password(pwd, salt) != db["users"][username]["password_hash"]:
			s("Incorrect password.")
			return False
		self.username = username
		s(f"Welcome, {username}!\n")
		return True

	def logout(self):
		self.username = None
		s("Logged out.\n")

	# Password vault
	def vault_add(self):
		if not self.username:
			s("Please login first.")
			return
		s("\nAdd website credentials")
		site = input("Website/App name>> ").strip()
		uid = input("Login username/email>> ").strip()
		pwd = safe_getpass("Password (stored as plain text) >> ")
		db = load_db()
		entry = {"site": site, "login": uid, "password": pwd}
		db["users"][self.username]["vault"].append(entry)
		save_db(db)
		s("Saved ✅\n")

	def vault_list(self):
		if not self.username:
			s("Please login first.")
			return
		db = load_db()
		items = db["users"][self.username]["vault"]
		if not items:
			s("No saved credentials yet.\n")
			return
		s("\nYour saved credentials:")
		for idx, item in enumerate(items, start=1):
			print(f"{idx}. {item['site']} | {item['login']} | {item['password']}")
		print()

	def vault_delete(self):
		if not self.username:
			s("Please login first.")
			return
		db = load_db()
		items = db["users"][self.username]["vault"]
		if not items:
			s("No items to delete.\n")
			return
		self.vault_list()
		choice = prompt_int("Select number to delete (0 to cancel)>> ")
		if choice == 0:
			return
		if 1 <= choice <= len(items):
			removed = items.pop(choice - 1)
			db["users"][self.username]["vault"] = items
			save_db(db)
			s(f"Deleted: {removed['site']}\n")
		else:
			s("Invalid selection.\n")

	# Messaging
	def send_message(self):
		if not self.username:
			s("Please login first.")
			return
		db = load_db()
		recipient = input("Send to (username)>> ").strip().lower()
		if recipient not in db["users"]:
			s("Recipient not found.")
			return
		msg = input("Message>> ")
		ts = datetime.utcnow().isoformat() + "Z"
		incoming = {"from": self.username, "message": msg, "ts": ts}
		outgoing = {"to": recipient, "message": msg, "ts": ts}
		db["users"][recipient]["inbox"].append(incoming)
		db["users"][self.username]["sent"].append(outgoing)
		save_db(db)
		s("Message sent ✅\n")

	def view_inbox(self):
		if not self.username:
			s("Please login first.")
			return
		db = load_db()
		inbox = db["users"][self.username]["inbox"]
		if not inbox:
			s("Inbox is empty.\n")
			return
		s("\nYour inbox:")
		for idx, m in enumerate(inbox, start=1):
			print(f"{idx}. From: {m['from']} | {m['ts']}\n   {m['message']}")
		print()

	def view_sent(self):
		if not self.username:
			s("Please login first.")
			return
		db = load_db()
		sent = db["users"][self.username]["sent"]
		if not sent:
			s("No sent messages.\n")
			return
		s("\nSent messages:")
		for idx, m in enumerate(sent, start=1):
			print(f"{idx}. To: {m['to']} | {m['ts']}\n   {m['message']}")
		print()


def main_menu(session):
	while True:
		s("What do you want to do?")
		s("1. Register")
		s("2. Login")
		s("3. Exit\n")
		choice = prompt_int("(1-3)>> ", {1, 2, 3})
		if choice == 1:
			session.register()
		elif choice == 2:
			if session.login():
				user_menu(session)
		elif choice == 3:
			s("Goodbye!")
			exit(0)


def user_menu(session):
	while session.username is not None:
		s("What next?")
		s("1. Add website credentials")
		s("2. List saved credentials")
		s("3. Delete a credential")
		s("4. Send a message")
		s("5. View inbox")
		s("6. View sent messages")
		s("7. Logout\n")
		choice = prompt_int("(1-7)>> ", {1, 2, 3, 4, 5, 6, 7})
		if choice == 1:
			session.vault_add()
		elif choice == 2:
			session.vault_list()
		elif choice == 3:
			session.vault_delete()
		elif choice == 4:
			session.send_message()
		elif choice == 5:
			session.view_inbox()
		elif choice == 6:
			session.view_sent()
		elif choice == 7:
			session.logout()


if __name__ == "__main__":
	session = Session()
	main_menu(session)
