import os
import json
import time

USERS_FILE = "users.json"
POSTS_FILE = "posts.json"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def load_json(file, default):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump(default, f)
        return default
    else:
        with open(file, 'r') as f:
            return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def signup(users):
    clear()
    print(Colors.OKGREEN + "📝 Sign Up" + Colors.ENDC)
    while True:
        username = input("Enter a username: ").strip()
        if username == '':
            print(Colors.FAIL + "Username cannot be empty." + Colors.ENDC)
            continue
        if username in users:
            print(Colors.FAIL + "Username already exists. Try another." + Colors.ENDC)
            continue
        users[username] = {"posts": [], "likes_received": 0}
        save_json(USERS_FILE, users)
        print(Colors.OKGREEN + f"User '{username}' created successfully!" + Colors.ENDC)
        time.sleep(1)
        return username

def login(users):
    clear()
    print(Colors.OKGREEN + "🔐 Login" + Colors.ENDC)
    while True:
        username = input("Enter username: ").strip()
        if username in users:
            print(Colors.OKGREEN + f"Welcome back, {username}!" + Colors.ENDC)
            time.sleep(1)
            return username
        else:
            print(Colors.FAIL + "Username not found. Try again or sign up." + Colors.ENDC)

def create_post(posts, username):
    clear()
    print(Colors.OKCYAN + "📝 Create New Post" + Colors.ENDC)
    content = input("Write your post (max 280 chars): ").strip()
    if content == '':
        print(Colors.FAIL + "Post content cannot be empty." + Colors.ENDC)
        time.sleep(1)
        return
    if len(content) > 280:
        print(Colors.FAIL + "Post too long. Limit 280 chars." + Colors.ENDC)
        time.sleep(1)
        return
    post = {
        "id": len(posts)+1,
        "author": username,
        "content": content,
        "likes": 0,
        "liked_by": []
    }
    posts.append(post)
    save_json(POSTS_FILE, posts)
    print(Colors.OKGREEN + "Post created successfully!" + Colors.ENDC)
    time.sleep(1)

def list_posts(posts):
    clear()
    print(Colors.HEADER + "📢 All Posts\n" + Colors.ENDC)
    if not posts:
        print("No posts yet. Be the first!")
        return
    for p in posts:
        print(f"{Colors.OKBLUE}[{p['id']}] {p['author']}: {Colors.ENDC}{p['content']}")
        print(f"   {Colors.WARNING}❤️ Likes: {p['likes']}{Colors.ENDC}")
        print("-"*40)

def like_post(posts, users, username):
    list_posts(posts)
    choice = input("Enter post ID to like or 'B' to go back: ").strip().lower()
    if choice == 'b':
        return
    if not choice.isdigit():
        print(Colors.FAIL + "Invalid input." + Colors.ENDC)
        time.sleep(1)
        return
    post_id = int(choice)
    for p in posts:
        if p['id'] == post_id:
            if username in p['liked_by']:
                print(Colors.WARNING + "You already liked this post." + Colors.ENDC)
                time.sleep(1)
                return
            p['likes'] += 1
            p['liked_by'].append(username)
            # Update author's likes_received
            author = p['author']
            if author in users:
                users[author]["likes_received"] += 1
                save_json(USERS_FILE, users)
            save_json(POSTS_FILE, posts)
            print(Colors.OKGREEN + "Post liked!" + Colors.ENDC)
            time.sleep(1)
            return
    print(Colors.FAIL + "Post not found." + Colors.ENDC)
    time.sleep(1)

def view_profile(users, username, posts):
    clear()
    print(Colors.OKGREEN + f"👤 Profile: {username}" + Colors.ENDC)
    user_data = users.get(username)
    if not user_data:
        print("User data not found.")
        return
    user_posts = [p for p in posts if p['author'] == username]
    print(f"Total posts: {len(user_posts)}")
    print(f"Total likes received: {user_data.get('likes_received', 0)}")
    print("\nYour Posts:")
    for p in user_posts:
        print(f"  [{p['id']}] {p['content']} (❤️ {p['likes']})")
    input("\nPress Enter to return to menu...")

def main_menu():
    users = load_json(USERS_FILE, {})
    posts = load_json(POSTS_FILE, [])

    clear()
    print(Colors.HEADER + Colors.BOLD + "🚀 Welcome to Terminal Social Media CLI" + Colors.ENDC)
    print("1. Login")
    print("2. Sign Up")
    print("3. Quit")

    while True:
        choice = input("Choose option: ").strip()
        if choice == '1':
            username = login(users)
            break
        elif choice == '2':
            username = signup(users)
            break
        elif choice == '3':
            print(Colors.OKGREEN + "👋 Bye! Thanks for visiting." + Colors.ENDC)
            exit(0)
        else:
            print(Colors.FAIL + "Invalid choice, try again." + Colors.ENDC)

    while True:
        clear()
        print(Colors.OKCYAN + f"👋 Hello, {username}!" + Colors.ENDC)
        print("1. Create Post 📝")
        print("2. View All Posts 📢")
        print("3. Like a Post ❤️")
        print("4. View Your Profile 👤")
        print("5. Logout 🔒")

        choice = input("Choose option: ").strip()
        if choice == '1':
            create_post(posts, username)
        elif choice == '2':
            list_posts(posts)
            input("\nPress Enter to return...")
        elif choice == '3':
            like_post(posts, users, username)
        elif choice == '4':
            view_profile(users, username, posts)
        elif choice == '5':
            print(Colors.OKGREEN + "Logged out successfully." + Colors.ENDC)
            time.sleep(1)
            main_menu()
            break
        else:
            print(Colors.FAIL + "Invalid choice, try again." + Colors.ENDC)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
