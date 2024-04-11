# 323_semester_project

We make a .exe and when the user clicks to run it, it brings up a menu that allows the user point at the game that the user wants to decrypt/disconnect from steam. After that it checks what drm the game uses and if it uses a steam drm we decrypt it using ([https://github.com/atom0s/Steamless](https://github.com/atom0s/Steamless "https://github.com/atom0s/Steamless")) and then modify some files and emulate it using ([https://gitlab.com/Mr_Goldberg/goldberg_emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator "https://gitlab.com/Mr_Goldberg/goldberg_emulator")).

(done) make .exe and gui that allows user to point at game folder user wants to decrypt/disconnect from steam

(done) integrate or use pcgamerwiki api to look at what drm the game has.

(done) if game has other drm other then those then report back can not emulate or decrypt.

(done) select .exe and install steamless if it doesnt exist and unzip

X if game has steam drm use steamless cli to decrypt

- Add: System only searches for "steam_api.dll" in find_game_dll(), and doesn't account for "steam_api64.dll". Make find_game_dll() search for "steam_api64.dll" too.

- Emulate button: Doesn't run the unpacked exe yet, but does file modifications with goldberg. Made it a separate GUI button for testing.

    X Add call to emulate unpacked game in main.py in emulate() (made a function in SteamDRMStripper to do that. It doesn't fit with that file, but we'll reorganize the code later.)

    X If a game has an original steam_api(64).dll file that's older than may 2016, then add the interface txt feature to the game directory. (See goldberg steam emulator readme file)

    X If there's time, account for Linux too? (Linux uses a .so file extention instead of .dll)

X If game doesnt have drm just emulate

X Organize code/abstract code! (I replicated some of the existing code because it wasn't abstract enough for me to use it with other features.)

X decorate gui

Other notes:
- There's a command that requires system to already have wsl to run the command. Is that an issue? See detect_bit_version() in emulate.py

**Usage:**

pip install requirements.txt

to build: pyinstaller --onefile --windowed main.py (.exe in dist folder)




    NOTE: 4/3/2024
    -Different button on GUI for unpacking the game exe because some games don't have the availability section on the gaming wiki, but can still be unpacked with steamless -- thus i made the functionalites separate for now. 
    (I was only able to find 1 game that I could unpack using steamless, which is the one that doesn't have the availability section on the wiki.)
        - I manually downloaded goldberg emulator and did the file modifications, so I was able to run the unpacked exe. But The application would open and then almost immediately close , then opened steam sign in page -- perhaps the game uses other anti-tamper measures too. I'm pretty sure it's not a steamless issue and that we can't do anything about this. *Find a game that is able to unpack and emulate*

    -Hard to find games that actually work with steamless. This is because most games layer with other DRMs too, or use DRMs other than SteamStub. Thus, cannot unpack these executable files -- *Find a way to see if games use other DRMs too or solely SteamStub*?.

