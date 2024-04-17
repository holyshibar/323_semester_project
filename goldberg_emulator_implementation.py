import os
import shutil
import requests


class GB_Modification:
    def __init__(self, game_dir, game_name):
        self.game_dir = game_dir
        self.game_name = game_name
        self.game_dll_path = self.find_game_dll()

    def find_game_dll(self):
        """Finds the path of the game's Dynamic Link Library (DLL file)."""

        current_dir = self.game_dir
        print("Current directory:", current_dir)
        # Loops through the directory and all subdirectories
        for root, dirs, files in os.walk(self.game_dir):
            for file in files:
                # Checks for either steam_api64.dll or steam_api.dll
                if file == "steam_api64.dll" or file == "steam_api.dll":
                    print(f"Found {file}")
                    # Returns the path to the found file
                    return os.path.join(root, file)
        # If no file is found, return None
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
        """Creates a TXT file containing the game's steam id."""

        game_dir = self.game_dir
        appid = self.find_appid()
        if not appid:
            print("Could not find Steam appid.")
            return
        else:
            # Checks to see if steam_appid.txt exists already
            appid_txt = os.path.join(game_dir, "steam_appid.txt")
            # If the TXT file doesn't exist, make it and write its app id to the file
            if not os.path.exists(appid_txt):
                with open(appid_txt, "w") as file:
                    file.write(appid)
                print(f"Successfully created steam_appid.txt in {game_dir}\n")
            else:
                print("steam_appid.txt already exists. Skipping step...\n")

    # Modifies the games files by backing up the original DLL file before replacing it with a modified DLL file from Goldberg folder
    def modify_files(self, goldberg_folder_path, dll_path, game_exe_path):
        dll_dir = os.path.dirname(dll_path)
        game_exe_path = os.path.dirname(game_exe_path)
        dll_file_name = os.path.basename(dll_path)

        print("DLL directory:", dll_dir)
        print("DLL file name:", dll_file_name)
        print("Game exe path:", game_exe_path)

        # Creates a backup directory
        backup_dir = os.path.join(dll_dir, "backup_dll_dir")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Moves and renames the original dll file to the backup directory
        backup_file_path = os.path.join(backup_dir, dll_file_name + ".bak")
        shutil.move(dll_path, backup_file_path)

        # Copies the corresponding file from the Goldberg folder
        source_file_path = os.path.join(goldberg_folder_path, dll_file_name)
        if os.path.exists(source_file_path):
            shutil.copy(source_file_path, dll_path)
        else:
            print(
                f"Error: The file {dll_file_name} was not found in the Goldberg folder.")

        # Creates a TXT file with the corresponding game's Steam Application ID
        appid_txt = self.add_appid_txt()

        print("Backedup original dll and replaced with goldberg")
        print("Created steam_appid.txt")
