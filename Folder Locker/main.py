import os

# Step 1: User se folder ka path lo
folder_path = input(">>: ")
r_p = "E:\\VHD's\\hi\\"
if folder_path.lower() == "r":
    folder_path = r_p
else:
    print("ERRROR")

# Step 2: Lock ya Unlock karna hai?
action = input("Type 'lock' to lock the folder or 'unlock' to unlock it: ").lower()

# Step 3: Password
password = "mera_secret"
# Step 4: Action logic
if action == "lock":
    user_pass = input("Enter password to LOCK: ")
    if user_pass == password:
        os.system(f'attrib +h +s "{folder_path}"')
        print("✅ Folder locked successfully!")
    else:
        print("❌ Incorrect password. Cannot lock.")
        
elif action == "unlock":
    user_pass = input("Enter password to UNLOCK: ")
    if user_pass == password:
        os.system(f'attrib -h -s "{folder_path}"')
        print("✅ Folder unlocked successfully!")
    else:
        print("❌ Incorrect password. Cannot unlock.")

else:
    print("⚠️ Invalid option. Type 'lock' or 'unlock'.")


 