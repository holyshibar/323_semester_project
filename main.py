import tkinter as tk
from tkinter import filedialog, scrolledtext
from drm_analysis import DRMAnalysis
import os
import sys
import io
import subprocess
import threading


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


def check_required_folder():
    # Gets the directory of the current script
    exe_path = os.path.dirname(os.path.abspath(__file__))
    required_folder = os.path.join(exe_path, "Steamless.v3.1.0.3.-.by.atom0s")
    if not os.path.exists(required_folder):
        print("Required folder not found. Running download_required.py...")
        # Assuming download_required.py is in the same directory as this script
        download_script_path = os.path.join(exe_path, "download_required.py")
        try:
            result = subprocess.run([sys.executable, download_script_path], check=True,
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Instead of print, directly insert into log_area
            log_area.insert(tk.END, result.stdout + "\n")
            if result.stderr:
                log_area.insert(tk.END, "Error: " + result.stderr + "\n")
        except subprocess.CalledProcessError as e:
            log_area.insert(
                tk.END, "Error running download_required.py:\n" + e.stderr + "\n")
    else:
        print("Required folder found. Skipping download...")


def browse_file():
    global folder_path, game_name
    file_path = filedialog.askopenfilename(
        filetypes=[("Executable files", "*.exe")])
    if file_path:
        # Extract the folder path and the game name from the file path
        folder_path = os.path.dirname(file_path)
        print("folder_path:", folder_path)
        game_name = os.path.basename(folder_path)
        print("game_name:", game_name)
        path_label.config(text=folder_path)
    else:
        path_label.config(text="No file selected")
        folder_path = None
        game_name = None


def decrypt():
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
        log_area.insert(tk.END, analysis_result)
    else:
        log_area.insert(
            tk.END, "Availability section not found or failed to retrieve data.\n")

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

log_stream = PrintLogger(log_area)
sys.stdout = log_stream

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Change at the end of your script, before mainloop
thread = threading.Thread(target=check_required_folder)
thread.start()

app.mainloop()
