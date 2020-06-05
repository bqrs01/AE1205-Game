"""
 File: powerup.py
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


>>> This module contains code for powerups.
"""

import pygame as pg
import os
import random
from .. import prepare, tools


class PowerupManager(pg.sprite.Group):
    def __init__(self, statsManager, *sprites):
        super().__init__(*sprites)
        self.statsManager = statsManager

    def new_powerup(self, center_pos):
        if (len(self) == 0) and not self.statsManager.powerup_active:
            self.add(Powerup(center_pos))
        else:
            print('there\'s already a powerup boi!')

    def update(self, *args):
        for powerup in self.sprites():
            powerup.update(*args)

    def draw(self, surface):
        for powerup in self.sprites():
            powerup.draw(surface)


class Powerup(tools._BaseSprite):
    def __init__(self, center_pos):
        super().__init__(center_pos, (75, 75))
        self.image, self.powerup = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = center_pos

    def get_image(self):
        powerup = random.choice(["x2", "infinity"])
        image = pg.image.load(os.path.join(
            os.getcwd(), f"src/images/powerup_{powerup}.png")).convert_alpha()
        return image, powerup

    def update(self, player, statsManager):
        collision = pg.sprite.collide_rect(player, self)
        if collision:
            if self.powerup == "x2":
                statsManager.set_multiplier(2.0)
            elif self.powerup == "infinity":
                statsManager.set_infinity()
            self.kill()
