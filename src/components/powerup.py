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

POWERUP_SIZE = (40, 40)


class PowerupManager(pg.sprite.Group):
    def __init__(self, statsManager, *sprites):
        super().__init__(*sprites)
        self.statsManager = statsManager

    def new_powerup(self, center_pos, health=False):
        if (len(self) == 0) and (not self.statsManager.powerup_active) and (self.statsManager.cooldown <= 0):
            self.add(Powerup(center_pos, health=health))
        else:
            print('there\'s already a powerup boi!')

    def update(self, *args):
        for powerup in self.sprites():
            powerup.update(*args)

    def draw(self, surface):
        for powerup in self.sprites():
            powerup.draw(surface)


class Powerup(tools._BaseSprite):
    def __init__(self, center_pos, health=False):
        super().__init__(center_pos, (75, 75))
        if not health:
            self.powerupImage, self.powerup = self.get_image()
        else:
            self.powerupImage = pg.image.load(os.path.join(
                os.getcwd(), f"src/images/powerup_heart.png")).convert_alpha()
            self.powerup = "health"
        self.blankImage = self.get_image(blank=True)
        self.rect = self.powerupImage.get_rect()
        self.rect.center = center_pos
        self.time_to_blink = 10000
        self.time_to_stop = 5000
        self.blink_cooldown = 150
        self.blink_on = False

    def get_image(self, blank=False):
        if blank:
            base = pg.Surface(POWERUP_SIZE, pg.SRCALPHA).convert()
            base.fill((255, 255, 0))
            base.set_colorkey((255, 255, 0))
            image = base.copy()
            return image
        else:
            powerup = random.choice(["x2", "infinity"])
            image = pg.image.load(os.path.join(
                os.getcwd(), f"src/images/powerup_{powerup}.png")).convert_alpha()
            return image, powerup

    def update(self, player, statsManager, dt):
        if self.time_to_blink > 0:
            self.time_to_blink -= dt
        else:
            # Start blinking and countdown to stop
            self.blink_cooldown -= dt
            if self.blink_cooldown <= 0:
                self.blink_on = not self.blink_on
                self.blink_cooldown = 150
            if self.time_to_stop > 0:
                self.time_to_stop -= dt
            else:
                # Stop blinking
                self.kill()

        if self.blink_on:
            self.image = self.blankImage
        else:
            self.image = self.powerupImage

        collision = pg.sprite.collide_rect(player, self)
        if collision:
            if self.powerup == "x2":
                statsManager.set_multiplier(2.0)
            elif self.powerup == "infinity":
                statsManager.set_infinity()
            elif self.powerup == "health":
                statsManager.addHealth(health=10)
            self.kill()
