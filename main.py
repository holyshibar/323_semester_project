import tkinter as tk
from tkinter import filedialog, scrolledtext
from drm_analysis import DRMAnalysis
import os
import sys
import io
import subprocess
import threading
import SteamDRMStripper
import download_required
from goldberg_emulator_implementation import GB_Modification


class PrintLogger(io.StringIO):
    def __init__(self, log_area):
        super().__init__()
        self.log_area = log_area

    def write(self, text):
        self.log_area.insert(tk.END, text)
        self.log_area.yview(tk.END)


# Store the folder_path and game_name globally
folder_path = None
game_name = None
game_file_path = None
steamless_folder_path = None
goldberg_folder_path = None


def check_required_folder():
    global steamless_folder_path, goldberg_folder_path
    try:
        # Gets the directory of the current script
        exe_path = os.path.dirname(os.path.abspath(__file__))

        # Check for Steamless folder
        steamless_folder_path = os.path.join(
            exe_path, "Steamless.v3.1.0.3.-.by.atom0s")
        if not os.path.exists(steamless_folder_path):
            log_area.insert(
                tk.END, "Steamless folder not found. Downloading Steamless...\n")
            # Assuming download_required.py is in the same directory as this script
            download_required.download_steamless()
        else:
            log_area.insert(
                tk.END, "Steamless folder found. Skipping Steamless download...\n")

        # Check for Goldberg folder
        goldberg_folder_path = os.path.join(
            exe_path, "Goldberg_Lan_Steam_Emu_v0.2.5")
        if not os.path.exists(goldberg_folder_path):
            log_area.insert(
                tk.END, "Goldberg folder not found. Downloading Goldberg Emulator...\n")
            download_required.download_goldberg()
        else:
            log_area.insert(
                tk.END, "Goldberg folder found. Skipping Goldberg Emulator download...\n")
    except Exception as e:
        log_area.insert(tk.END, f"Error: {e}\n")


def browse_file():
    global folder_path, game_name, game_file_path
    game_file_path = filedialog.askopenfilename(
        filetypes=[("Executable files", "*.exe")])
    if game_file_path:
        # Extract the folder path and the game name from the file path
        folder_path = os.path.dirname(game_file_path)
        print("folder_path:", folder_path)
        game_name = os.path.basename(folder_path)
        print("game_name:", game_name)
        path_label.config(text=folder_path)
    else:
        path_label.config(text="No file selected")
        folder_path = None
        game_name = None


# def decrypt():

#     """Analyzes DRM of the game."""

#     global game_name
#     if not game_name:
#         log_area.insert(tk.END, "Please select a folder first.\n")
#         return

#     log_area.insert(tk.END, f"Analyzing {game_name}...\n")
#     drm_analysis = DRMAnalysis(game_name)
#     availability_section, denuvo_detected = drm_analysis.get_pcgamingwiki_info()

#     if denuvo_detected:
#         log_area.insert(tk.END, "Denuvo Anti-Tamper detected.\n")
#     elif availability_section:
#         analysis_result = drm_analysis.analyze_steam_availability(
#             availability_section)
#         log_area.insert(tk.END, analysis_result)
#     else:
#         log_area.insert(
#             tk.END, "Availability section not found or failed to retrieve data.\n")

#     log_area.yview(tk.END)


def decrypt():
    """Searches pcgamingwikifor info, unpacks() if needed, and emulates()."""

    global game_name
    if not game_name:
        log_area.insert(tk.END, "Please select a folder first.\n")
        return

    log_area.insert(tk.END, f"Analyzing {game_name}...\n")
    drm_analysis = DRMAnalysis(game_name)
    availability_section, denuvo_detected = drm_analysis.get_pcgamingwiki_info()
    if denuvo_detected:
        log_area.insert(tk.END, "Denuvo Anti-Tamper detected.\n")
    elif availability_section:
        analysis_result = drm_analysis.analyze_steam_availability(
            availability_section)
        # Run Steamless if game doesn't use DRM
        if "Doesn't use DRM" not in analysis_result:
            log_area.insert(tk.END, f"Unpacking {game_name}...\n")
            if steamless_folder_path:
                unpacked_file_path = SteamDRMStripper.unpack_with_steamless(
                    game_file_path, steamless_folder_path)
            else:
                log_area.insert(
                    tk.END, "Steamless folder not found. Unable to unpack.\n")

        # Emulate game
        if unpacked_file_path:
            emulate_game = emulate(unpacked_file_path)
        else:
            emulate_game = emulate(game_file_path)
        log_area.insert(tk.END, analysis_result)
        log_area.insert(tk.END, "DONE")

    else:
        log_area.insert(
            tk.END, "Availability section not found or failed to retrieve data.\n")

    log_area.yview(tk.END)

# Unpack and run the unpacked file if applicable


def unpack():
    global game_name, steamless_folder_path, game_file_path
    if not game_name:
        log_area.insert(tk.END, "Please select a folder first.\n")
        return
    log_area.insert(tk.END, f"Unpacking {game_name}...\n")
    if steamless_folder_path:
        unpacked_file_path = SteamDRMStripper.unpack_with_steamless(
            game_file_path, steamless_folder_path)
    else:
        log_area.insert(
            tk.END, "Steamless folder not found. Unable to unpack.\n")
    log_area.yview(tk.END)


def emulate(game_exe_path):
    log_area.insert(tk.END, f"Analyzing bit version of {game_name}...\n")
    gb_analysis = GB_Modification(folder_path, game_name)
    bit_version = gb_analysis.detect_bit_version()

    # if bit_version["windows_64"] == True or bit_version["windows_32"]==True:
    if bit_version["windows_32"] == True:
        log_area.insert(tk.END, f"Bit version: {bit_version}\n")
        log_area.insert(tk.END, f"Preparing to emulate {game_name}...\n")
        dll_dir = gb_analysis.find_game_dll()
        if dll_dir:
            log_area.insert(tk.END, "Game dll found.\n")
            log_area.insert(tk.END, "Modifying dll file.\n")
            modify_files = gb_analysis.modify_files(
                goldberg_folder_path, bit_version)
            run_game = SteamDRMStripper.run_unpacked_file(
                game_exe_path)  # Game can be unpacked or not
        else:
            log_area.insert(tk.END, "Game dll not found.\n")
    else:
        log_area.insert(
            tk.END, "Bit version unknown, or game is incompatible.\n")
    log_area.yview(tk.END)


app = tk.Tk()
app.title('Game Folder Selector')

log_area = scrolledtext.ScrolledText(app, width=40, height=10, state='normal')
log_area.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

path_label = tk.Label(app, text="No folder selected")
path_label.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

button_frame = tk.Frame(app)
button_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

browse_button = tk.Button(button_frame, text="Browse", command=browse_file)
browse_button.grid(row=0, column=0, padx=5)

decrypt_button = tk.Button(button_frame, text="Decrypt", command=decrypt)
decrypt_button.grid(row=0, column=1, padx=5)

# unpack_button = tk.Button(button_frame, text="Unpack", command=unpack)
# unpack_button.grid(row=0, column=2, padx=5)

# goldberg_button = tk.Button(button_frame, text="Emulate", command=emulate)
# goldberg_button.grid(row=0, column=3, padx=5)

log_stream = PrintLogger(log_area)
sys.stdout = log_stream

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Change at the end of your script, before mainloop
thread = threading.Thread(target=check_required_folder)
thread.start()

app.mainloop()
