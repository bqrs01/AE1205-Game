"""
This module initializes the pygame display.
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
