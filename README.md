# 323_semester_project

We make a .exe and when the user clicks to run it, it brings up a menu that allows the user point at the game that the user wants to decrypt/disconnect from steam. After that it checks what drm the game uses and if it uses a steam drm we decrypt it using ([https://github.com/atom0s/Steamless](https://github.com/atom0s/Steamless "https://github.com/atom0s/Steamless")) and then modify some files and emulate it using ([https://gitlab.com/Mr_Goldberg/goldberg_emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator "https://gitlab.com/Mr_Goldberg/goldberg_emulator")).

(done) make .exe and gui that allows user to point at game folder user wants to decrypt/disconnect from steam

(done) integrate or use pcgamerwiki api to look at what drm the game has.

(done) if game has other drm other then those then report back can not emulate or decrypt.

(done) select .exe and install steamless if it doesnt exist and unzip

(done) if game has steam drm use steamless cli to decrypt

- Add: System only searches for "steam_api.dll" in find_game_dll(), and doesn't account for "steam_api64.dll". Make find_game_dll() search for "steam_api64.dll" too.

    (done) Add call to emulate unpacked game in main.py in emulate() (made a function in SteamDRMStripper to do that. It doesn't fit with that file, but we'll reorganize the code later.)

    X If a game has an original steam_api(64).dll file that's older than may 2016, then add the interface txt feature to the game directory. (See goldberg steam emulator readme file)

    X If there's time, account for Linux too? (Linux uses a .so file extention instead of .dll)

(done) If game doesnt have drm just emulate

X Organize code/abstract code! (I replicated some of the existing code because it wasn't abstract enough for me to use it with other features.)

X decorate gui

Other notes:
- There's a command that requires system to already have wsl to run the command. Is that an issue? See detect_bit_version() in emulate.py

**Usage:**

pip install requirements.txt

to build: pyinstaller --onefile --windowed main.py (.exe in dist folder)
