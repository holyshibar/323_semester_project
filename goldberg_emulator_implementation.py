import os
import shutil
import subprocess
import requests


class GB_Modification:
    def __init__(self, game_dir, game_name):
        self.game_dir = game_dir
        self.game_name = game_name
        self.game_dll_path = self.find_game_dll()

    def find_game_dll(self):
        """Finds the path of the game's dll file."""

        current_dir = self.game_dir
        print("Current directory:", current_dir)
        dll_path = os.path.join(current_dir, "steam_api64.dll")
        dll_path = os.path.normpath(dll_path)
        # Check if the DLL exists in the current directory
        if os.path.exists(dll_path):
            print(f"dll path in current directory: {dll_path}")
            print("dll path found.")
            return dll_path

        # If not found, search in all nested folders
        for root, dirs, files in os.walk(current_dir):
            if "steam_api64.dll" in files:
                dll_path = os.path.join(root, "steam_api64.dll")
                print(f"dll path: {dll_path}")
                print("dll path found in nested folder.")
                return dll_path

        print("dll path not found.")
        return None

    def backup_game_dll(self):
        """If the folder doesn't exist already, then create a folder called 'Backups' in the game's directory."""

        dll_path = self.game_dll_path
        current_dir = self.game_dir
        if dll_path:
            backup_dir = os.path.join(current_dir, "Backups")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            backup_file = os.path.join(backup_dir, os.path.basename(dll_path))
            shutil.move(dll_path, backup_file)
            return backup_file
        else:
            return None

    def detect_bit_version(self):
        """Detects the bit version of the game's dll file."""

        game_dir = self.game_dir
        bit_version = {
            "windows_64": False,
            "windows_32": False
        }
        os.chdir(game_dir)
        print("current directory", os.getcwd())
        try:
            result = subprocess.run(
                ["wsl", "file", "steam_api64.dll"], capture_output=True, text=True)
            output = result.stdout
            print(f"detecting bit version: {output}")
            if result.returncode != 0:
                print("Error:", result.stderr)
                return None
            else:
                if "x86_64" in output:
                    bit_version["windows_64"] = True
                    print("64-bit version")
                elif "Intel 80386" in output:
                    bit_version["windows_32"] = True
                    print("32-bit version")
                elif "P" in output:
                    bit_version["windows_64"] = True
                    print("windows_64 version")
                return bit_version

        except Exception as e:
            print("Error:", e)
            return None

    def find_appid(self):
        """Finds the game's steam id on pcgamingwiki.com."""

        params = {
            "action": "parse",
            "format": "json",
            "page": self.game_name,
            "prop": "wikitext"
        }
        response = requests.get(
            "https://www.pcgamingwiki.com/w/api.php", params=params)
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print("Error: ", data['error']['info'])
                return None
            elif 'parse' in data:
                wikitext = data['parse']['wikitext']['*']
                steam_appid_index = wikitext.find("|steam appid")
                if steam_appid_index != -1:
                    start_index = wikitext.find("=", steam_appid_index)
                    if start_index != -1:
                        end_index = wikitext.find("\n", start_index)
                        if end_index != -1:
                            appid = wikitext[start_index +
                                             1: end_index]. strip()
                            return appid
                        else:
                            print("Could not find the end of steamp_appid line")
                            return None
                    else:
                        print("Could not find the start of the steam_appid line")
                        return None
                else:
                    print("Steam appid not found.")
                    return None
        else:
            return None

    def add_appid_txt(self):
        """Creates a txt file containing the game's steam id."""

        game_dir = self.game_dir
        appid = self.find_appid()
        if not appid:
            print("Could not find Steam appid.")
            return
        else:
            # Check to see if steam_appid.txt exists already
            appid_txt = os.path.join(game_dir, "steam_appid.txt")
            # if the txt file doesn't exist, make it and write its app id to the file
            if not os.path.exists(appid_txt):
                with open(appid_txt, "w") as file:
                    file.write(appid)
                print(f"Successfully created steam_appid.txt in {game_dir}\n")
            else:
                print("steam_appid.txt already exists. Skipping step...\n")

    def modify_files(self, goldberg_folder_path, bit_version):
        """Moves the original game's dll file into a backup folder. If the game is a 32-bit game, it copies over the steam_api64.dll file
        from the goldberg directory into the game's directory, and creates a txt file with containing the steam id in the game's directory."""

        # Move original game dll into a backup folder
        backup_dll_path = self.backup_game_dll()
        if backup_dll_path is None:
            print("Could not backup game dll file.")
            return
        # Find the game's corresponding dll file from Goldberg folder
        if bit_version["windows_32"] == True:
            dll = os.path.join(goldberg_folder_path, "steam_api64.dll")
        # elif bit_version["windows_64"] == True:
        #     dll = os.path.join(goldberg_folder_path, "steam_api64.dll")
        # elif bit_version["linux_64"] == True:
        #     dll = os.path.join(goldberg_folder_path, "linux", "x86", "libsteam_api.so")
        # elif bit_version["linux_32"] == True:
        #     dll = os.path.join(goldberg_folder_path, "linux", "x86_64", "libsteam_api.so")
        else:
            print("Could not detect bit verison.")
        # Copy Goldberg's dll file into the game folder
        game_dir = self.game_dir
        try:
            shutil.copy(dll, game_dir)
            print(f"Successfully copied {os.path.basename(dll)} to {game_dir}")
            # Make steam_appid.txt if there isn't already one
            appid_txt = self.add_appid_txt()
        except Exception as e:
            print("Error:", e)
