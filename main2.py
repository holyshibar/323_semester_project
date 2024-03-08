import tkinter as tk
from tkinter import filedialog, scrolledtext
from drm_analysis import DRMAnalysis  # Ensure to import the DRMAnalysis class
import os


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:  # Check if a folder was actually selected
        # Extracts the name of the game from the folder path
        game_name = os.path.basename(folder_path)
        # Set the extracted game name as the label text
        path_label.config(text=game_name)
    else:
        path_label.config(text="No folder selected")


def decrypt():
    # This now gets the extracted game name
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

decrypt_button = tk.Button(app, text="Decrypt", command=decrypt)
decrypt_button.pack()

app.mainloop()