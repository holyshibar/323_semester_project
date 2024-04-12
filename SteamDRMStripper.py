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
            run_steamless = subprocess.run([steamless_cli_path, game_exe_path], capture_output=True, text=True)
            if run_steamless.returncode != 0:
                print("Error:", run_steamless.stderr) #Error message may be empty
            else:
                print("Successfully unpacked file.")
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
    for file in files:
        if file.endswith(".exe") and ".unpacked" in file:
            return os.path.join(game_dir, file)
    return None

def run_unpacked_file(file_path):
    try:
        subprocess.run([file_path])
    except Exception as e:
        print("Error:", e)

