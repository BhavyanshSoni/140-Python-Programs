import subprocess
import re

def get_wifi_profiles():
    profiles_data = subprocess.check_output("netsh wlan show profiles", shell=True).decode()
    profiles = re.findall("All User Profile     : (.*)", profiles_data)
    return profiles

def get_wifi_password(profile_name):
    try:
        profile_info = subprocess.check_output(f"netsh wlan show profile name=\"{profile_name}\" key=clear", shell=True).decode()
        password = re.search("Key Content            : (.*)", profile_info)
        if password:
            return password.group(1)
        else:
            return "not found"
    except:
        return "error"

def main():
    profiles = get_wifi_profiles()
    print("Saved Wi-Fi Networks:\n------------------------")
    with open("wifi_passwords_log.txt", "w") as file:
        for profile in profiles:
            password = get_wifi_password(profile)
            log = f"{profile} => Password: {password}"
            print(log)
            file.write(log + "\n")

if __name__ == "__main__":
    main()
