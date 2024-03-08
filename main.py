# rm -r .\build\, .\dist\, .\main.spec
# pyinstaller --onefile --windowed main.py

import tkinter as tk
from tkinter import filedialog, scrolledtext


def browse_folder():
    folder_path = filedialog.askdirectory()
    path_label.config(text=folder_path)


def decrypt():
    # Example logs
    logs = ["This is a test", "loading....."]
    for log in logs:
        log_area.insert(tk.END, log + "\n")
    log_area.yview(tk.END)  # Auto-scroll to the end


app = tk.Tk()
app.title('Game Folder Selector')

# Browse button
browse_button = tk.Button(app, text="Browse", command=browse_folder)
browse_button.pack()

# Path label
path_label = tk.Label(app, text="No folder selected")
path_label.pack()

# Log area
log_area = scrolledtext.ScrolledText(app, width=40, height=10, state='normal')
log_area.pack(pady=10)

# Decrypt button
decrypt_button = tk.Button(app, text="Decrypt", command=decrypt)
decrypt_button.pack()

app.mainloop()
