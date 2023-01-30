import json
import os
import pathlib
import time

import profig

DEBUG = False
pathlib.Path(os.getenv("HOME") + "/.CMAN").touch()

config = profig.Config(pathlib.Path(os.getenv("HOME") + "/.CMAN").__str__())
game = config.section("GAME")

# DEBUG
if DEBUG:
    # GAME PATH
    t = pathlib.Path(f"/tmp/test_CMAN_{time.time()}")
    t.mkdir()
    GAME_PATH = t.__str__()
else:
    # GAME PATH
    try:
        GAME_PATH: str = game["PATH"]
    except profig.InvalidSectionError:
        config.init("GAME.PATH", f'{os.getenv("HOME")}/.minecraft/')
        config.write()

        GAME_PATH: str = game["PATH"]

GAME_PATH = pathlib.Path(GAME_PATH)
MODS_PATH = pathlib.Path(GAME_PATH, "mods")
