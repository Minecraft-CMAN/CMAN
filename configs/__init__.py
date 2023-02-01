import json
import os
import pathlib
import time

import profig

DEBUG = True
pathlib.Path(os.getenv("HOME") + "/.CMAN").touch()

config = profig.Config(pathlib.Path(os.getenv("HOME") + "/.CMAN").__str__())
config.sync()

game = config.section("GAME")

try:
    cfg = config.as_dict()["CMAN"]["last_startup"]
except:
    # first startup
    config.init("GAME.PATH", f'{os.getenv("HOME")}/.minecraft/')
    config.init("CMAN.last_startup", time.time())
    config.init(
        "CMAN.launchermeta",
        "https://bmclapi2.bangbang93.com",
    )

    print("This is first startup")

config.section("CMAN")["last_startup"] = time.time()

# DEBUG
if DEBUG:
    # GAME PATH
    t = pathlib.Path(f"/tmp/test_CMAN")
    t2 = pathlib.Path(f"/tmp/test_CMAN_meta")

    GAME_PATH = t.__str__()
    META_PATH = t2.__str__()
else:
    # GAME PATH
    GAME_PATH: str = game["PATH"]

GAME_PATH = pathlib.Path(GAME_PATH)
MODS_PATH = pathlib.Path(GAME_PATH, "mods")
LAUNCHER_META = config.as_dict()["CMAN"]["launchermeta"]

# make dir
try:
    GAME_PATH.mkdir()
    MODS_PATH.mkdir()
except FileExistsError:
    pass

# save
config.write()
