"""
This module initializes the pygame display.
"""

import os
import pygame as pg

from . import tools


pg.init()

SCREEN_SIZE = (1200, 700)
ORIGINAL_CAPTION = "AE1205 Game"

pg.display.set_caption(ORIGINAL_CAPTION)
_screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.update()


def get_screen():
    return _screen
