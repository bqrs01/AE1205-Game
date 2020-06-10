"""
 File: prepare.py
 Authors: Mario Padrón Tardáguila & Bryan Quadras
 
 Copyright (c) 2020 Mario Padrón Tardáguila & Bryan Quadras
 
 The MIT License
 
 Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute, 
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
 is furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all copies 
 or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
 PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
 FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 

>>> This module initializes the pygame display and sets some game wide constants.
"""

import os
import pygame as pg
import platform

from . import tools

if platform.system() == "Windows":
    import ctypes
    # Workaround to display game icon in Windows Taskbar
    gameid = 'com.firecraze.game.final'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(gameid)

pg.init()

SCREEN_SIZE = (1200, 700)
SCREEN_CENTER = (600, 350)
ORIGINAL_CAPTION = "Firecraze (by Mario and Bryan)"
ORIGINAL_ICON_FILENAME = "redplain.png"

STARTING_POS = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

DEFAULT_CONTROLS = {
    pg.K_a: "left",
    pg.K_d: "right",
    pg.K_w: "up",
    pg.K_s: "down",
    pg.MOUSEBUTTONDOWN: "space"
}

DIRECT_DICT = {"down": (0, 1),
               "up": (0, -1),
               "left": (-1, 0),
               "right": (1, 0)}

pg.display.set_caption(ORIGINAL_CAPTION)


_screen = pg.display.set_mode(SCREEN_SIZE)

icon = pg.image.load(os.path.join(
    os.getcwd(), f"src/images/{ORIGINAL_ICON_FILENAME}")).convert_alpha()
icon = pg.transform.scale(icon, (31, 32))
pg.display.set_icon(icon)

pg.display.update()


def get_screen():
    return _screen
