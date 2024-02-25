"""
Name: Workers & Resources: Soviet Republic Mods SteamID Changer 
Author: Nedim Karahmetovic
Description: A tool to mass update/change SteamID in Workers & Resources: Soviet Republic mods.
Version: 1.0a
URL: https://github.com/TeraflopsBH/WRSR-Mods-SteamID-Changer
License: aGPL License
Icon: modler.ico
"""
import os
import re
import tkinter as tk
from tkinter import filedialog
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

CONFIG_FILE = "config.ini"

def clear_screen():
    """Clears the screen."""
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Linux and macOS
        os.system('clear')

#def load_config():
#    config = {
#        "OWNER_ID": None,
#        "MODS_FOLDER": None
#    }
#    if os.path.exists(CONFIG_FILE):
#        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
#            for line in f:
#                key, value = line.strip().split(" = ")
#                config[key] = value
#    return config

def load_config():
    config = {
        "OWNER_ID": None,
        "MODS_FOLDER": None
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if " = " in line:
                    key, value = line.strip().split(" = ")
                    value = value.strip()
                    if value.lower() == "none":  # Check if value is "None" (case insensitive)
                        value = None
                    config[key.strip()] = value
    return config

#def save_config(config):
#    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
#        for key, value in config.items():
#            f.write(f"{key} = {value}\n")

def save_config(config):
    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
        for key, value in config.items():
            if not value:  # Check if value is empty or None
                value = "None"
            f.write(f"{key} = {value}\n")

def update_owner_id(root_folder, new_owner_id):
    for folder, _, files in os.walk(root_folder):
        for file in files:
            if file == "workshopconfig.ini":
                file_path = os.path.join(folder, file)
                update_file(file_path, new_owner_id)

def update_file(file_path, new_owner_id):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if "$OWNER_ID" in line:
                updated_line = re.sub(r'\$OWNER_ID\s+\d+', f'$OWNER_ID {new_owner_id}', line)
                f.write(updated_line.rstrip('\r\n') + '\n')
            else:
                f.write(line.rstrip('\r\n') + '\n')

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select folder containing mods")
    return folder_selected

#def get_new_owner_id():
#    new_owner_id = input("\nEnter your SteamID: ")
#    return new_owner_id

def get_new_owner_id():
    new_owner_id = input("\nEnter your " + Fore.GREEN + "SteamID: "+ Style.RESET_ALL)
    if not new_owner_id.strip():  # Check if the entered SteamID is blank
        print("\n" + Fore.GREEN + "SteamID" + Style.RESET_ALL + " cleared sucessfully\n")
    else:
        print("\n" + Fore.GREEN + "SteamID" + Style.RESET_ALL + " set sucessfully\n")
    return new_owner_id

def set_owner_id(config):
    new_owner_id = get_new_owner_id()
    config["OWNER_ID"] = new_owner_id
    save_config(config)

def set_mods_folder(config):
    folder_selected = select_folder()
    if folder_selected and folder_selected != 'None':
        config["MODS_FOLDER"] = folder_selected
        save_config(config)

def change_mods_owner_id(config):
    if config["OWNER_ID"] and config["MODS_FOLDER"] and config["MODS_FOLDER"] != 'None':
        update_owner_id(config["MODS_FOLDER"], config["OWNER_ID"])
        print("\nAll mods configuration files updated with current " + Fore.GREEN + "SteamID" + Style.RESET_ALL)
    else:
        print("\n" + Fore.GREEN + "SteamID" + Style.RESET_ALL + " or Mods folder not set properly.")

def modify_owner_id(config):
    set_owner_id(config)

def update_mods_folder(config):
    set_mods_folder(config)

def main_menu(config):
    clear_screen()
    print("\n\n" + Fore.RED + "Workers & Resources: Soviet Republic\n" + Style.RESET_ALL)
    print("Mods " + Fore.GREEN + "SteamID" + Style.RESET_ALL + " Changer v1.0a - by " + Fore.GREEN + "TeraflopsBH" + Style.RESET_ALL + "\n")
    print(Fore.YELLOW + "https://github.com/TeraflopsBH/WRSR-Mods-SteamID-Changer" + Style.RESET_ALL)
    print("\n\n")
    while True:
        print("\n" + Fore.BLUE + "Menu:\n" + Style.RESET_ALL)
        options = []

        if not config["OWNER_ID"]:
            options.append(("Set your " + Fore.GREEN + "SteamID" + Style.RESET_ALL, set_owner_id))
        if not config["MODS_FOLDER"] or config["MODS_FOLDER"] == 'None':
            options.append(("Set or change mods folder location", set_mods_folder))
        if config["OWNER_ID"] and config["MODS_FOLDER"] and config["MODS_FOLDER"] != 'None':
            options.append(("Change all mods " + Fore.GREEN + "SteamID" + Style.RESET_ALL + " to: " + config["OWNER_ID"], change_mods_owner_id))
            options.append(("Modify current " + Fore.GREEN + "SteamID" + Style.RESET_ALL, modify_owner_id))
            options.append(("Update mods folder location", update_mods_folder))

        options.append((Fore.RED + "Exit" + Style.RESET_ALL, None))

        if not options:
            print("\n\n" + Fore.GREEN + "All options are set. Exiting.\n" + Style.RESET_ALL)
            break

        for index, (option_text, _) in enumerate(options, 1):
            print(f"{index}. {option_text}")

        choice = input("\n" + Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(options) - 1:
                selected_option = options[choice - 1]
                selected_option[1](config)
            elif choice == len(options):
                print("\n" + Fore.RED + "Exiting..." + Style.RESET_ALL)
                break
            else:
                print("\n" + Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
        else:
            print("\n" + Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

if __name__ == "__main__":
    config = load_config()
    main_menu(config)
