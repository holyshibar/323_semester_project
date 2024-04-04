# 323_semester_project

We make a .exe and when the user clicks to run it, it brings up a menu that allows the user point at the game that the user wants to decrypt/disconnect from steam. After that it checks what drm the game uses and if it uses a steam drm we decrypt it using ([https://github.com/atom0s/Steamless](https://github.com/atom0s/Steamless "https://github.com/atom0s/Steamless")) and then modify some files and emulate it using ([https://gitlab.com/Mr_Goldberg/goldberg_emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator "https://gitlab.com/Mr_Goldberg/goldberg_emulator")).

(done) make .exe and gui that allows user to point at game folder user wants to decrypt/disconnect from steam

(done) integrate or use pcgamerwiki api to look at what drm the game has.

(done) if game has other drm other then those then report back can not emulate or decrypt.

(done) select .exe and install steamless if it doesnt exist and unzip

X if game has steam drm use steamless cli to decrypt

    NOTE: 4/3/2024
    -Different button on GUI for unpacking the game exe because some games don't have the availability section on the gaming wiki, but can still be unpacked with steamless -- thus i made the functionalites separate for now. 
    (I was only able to find 1 game that I could unpack using steamless, which is the one that doesn't have the availability section on the wiki.)
        - I manually downloaded goldberg emulator and did the file modifications, so I was able to run the unpacked exe. But The application would open and then almost immediately close , then opened steam sign in page -- perhaps the game uses other anti-tamper measures too. I'm pretty sure it's not a steamless issue and that we can't do anything about this. *Find a game that is able to unpack and emulate*

    -Hard to find games that actually work with steamless. This is because most games layer with other DRMs too, or use DRMs other than SteamStub. Thus, cannot unpack these executable files -- *Find a way to see if games use other DRMs too or solely SteamStub*?.

    - Created the function to run the unpacked exe but haven't automated goldberg and file modifications yet


X If game doesnt have drm just emulate

X decorate gui

**Usage:**

pip install requirements.txt

to build: pyinstaller --onefile --windowed main.py (.exe in dist folder)
