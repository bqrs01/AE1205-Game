"""
 File: prepare.py
 Authors: Mario Padrón Tardáguila & Bryan Quadras
 
 Copyright (c) 2020 Mario Padrón Tardáguila & Bryan Quadras
 
 MIT License
 
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

from . import tools


pg.init()

SCREEN_SIZE = (1200, 700)
ORIGINAL_CAPTION = "AE1205 Game"

STARTING_POS = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)

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
pg.display.update()


def get_screen():
    return _screen
