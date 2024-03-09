import tkinter as tk
from tkinter import filedialog, scrolledtext
from drm_analysis import DRMAnalysis
import os
import sys
import io


class PrintLogger(io.StringIO):
    def __init__(self, log_area):
        super().__init__()
        self.log_area = log_area

    def write(self, text):
        self.log_area.insert(tk.END, text)
        self.log_area.yview(tk.END)


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        game_name = os.path.basename(folder_path)
        path_label.config(text=game_name)
    else:
        path_label.config(text="No folder selected")


def decrypt():
    game_name = path_label.cget("text")
    if game_name == "No folder selected":
        log_area.insert(tk.END, "Please select a folder first.\n")
        return

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

browse_button = tk.Button(app, text="Browse", command=browse_folder)
browse_button.pack()

path_label = tk.Label(app, text="No folder selected")
path_label.pack()

log_area = scrolledtext.ScrolledText(app, width=40, height=10, state='normal')
log_area.pack(pady=10)

log_stream = PrintLogger(log_area)
sys.stdout = log_stream

decrypt_button = tk.Button(app, text="Decrypt", command=decrypt)
decrypt_button.pack()

app.mainloop()
