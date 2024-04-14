import os
import subprocess


def find_steamless_cli(steamless_path):
    current_dir = steamless_path
    exe_path = os.path.join(current_dir, "Steamless.CLI.exe")
    if os.path.exists(exe_path):
        return exe_path
    return None


def unpack_with_steamless(game_exe_path, steamless_path):
    steamless_cli_path = find_steamless_cli(steamless_path)
    if steamless_cli_path:
        print("Steamless CLI found at:", steamless_cli_path)
        try:
            run_steamless = subprocess.run(
                [steamless_cli_path, game_exe_path], capture_output=True, text=True)
            if run_steamless.returncode != 0:
                # Error message may be empty
                # print("Error:", run_steamless.stderr)
                print("Does not contain SteamStub.")
            else:
                print("Contains SteamStub and Decrypted it")
                unpacked_file_path = find_unpacked_file(game_exe_path)
                if unpacked_file_path:
                    print("Unpacked file:", unpacked_file_path)
                    return unpacked_file_path
                else:
                    print("Unpacked file not found.")
                    return None
        except Exception as e:
            print("Error:", e)
    else:
        print("Steamless CLI not found.")


def find_unpacked_file(game_exe_path):
    game_dir = os.path.dirname(game_exe_path)
    files = os.listdir(game_dir)
    backup_dir = os.path.join(game_dir, "backup_game_dir")

    # Ensure the backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for file in files:
        if file.endswith(".exe") and ".unpacked" in file:
            print("Unpacked file found:", file)
            print("Backing up original file...")

            # Form the full path for the backup file
            original_file_full_path = os.path.join(
                game_dir, os.path.basename(game_exe_path))
            backup_file_full_path = os.path.join(
                backup_dir, os.path.basename(game_exe_path) + ".bak")

            # Rename and move the original executable to the backup directory
            os.rename(original_file_full_path, backup_file_full_path)

            # Rename the unpacked file to the original executable name
            unpacked_file_full_path = os.path.join(game_dir, file)
            os.rename(unpacked_file_full_path, original_file_full_path)

            print("Original file backed up to:", backup_file_full_path)
            print("Unpacked file renamed to:", original_file_full_path)
            print("Finished with Steamless processing")
            return original_file_full_path
    return None


def run_unpacked_file(file_path):
    try:
        subprocess.run([file_path])
    except Exception as e:
        print("Error:", e)
