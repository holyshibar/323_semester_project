# 323_semester_project

We make a .exe and when the user clicks to run it, it brings up a menu that allows the user point at the game that the user wants to decrypt/disconnect from steam. After that it checks what drm the game uses and if it uses a steam drm we decrypt it using ([https://github.com/atom0s/Steamless](https://github.com/atom0s/Steamless "https://github.com/atom0s/Steamless")) and then modify some files and emulate it using ([https://gitlab.com/Mr_Goldberg/goldberg_emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator "https://gitlab.com/Mr_Goldberg/goldberg_emulator")).

(almost done. Need to redirect stdout to the log area of the gui)make .exe and gui that allows user to point at game folder user wants to decrypt/disconnect from steam

(done) integrate or use pcgamerwiki api to look at what drm the game has.

X if game has steam drm use steamless cli to decrypt

X If game doesnt have drm just emulate

(done) if game has other drm other then those then report back can not emulate or decrypt.

**Usage:**

pip install requirements.txt

to build: pyinstaller --onefile --windowed main.py (.exe in dist folder)
