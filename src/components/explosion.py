"""
 File: explosion.py
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


>>> This module contains code for explosion animations.
"""

import pygame as pg
import os
from .. import prepare, tools


class ExplosionManager(pg.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.explosion_images = []
        for idx in range(9):
            image = pg.image.load(
                os.path.join(os.getcwd(), f"src/images/regularExplosion0{idx}.png")).convert()
            image.set_colorkey((0, 0, 0))
            image = pg.transform.scale(image, (75, 75))
            self.explosion_images.append(image)

    def new_explosion(self, center_pos):
        self.add(Explosion(center_pos, self.explosion_images))

    def update(self, *args):
        for explosion in self.sprites():
            explosion.update(*args)

    def draw(self, surface):
        for explosion in self.sprites():
            explosion.draw(surface)


class Explosion(tools._BaseSprite):
    def __init__(self, center_pos, expl_imgs):
        super().__init__(center_pos, (75, 75))
        self.expl_imgs = expl_imgs
        self.image = expl_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.center = center_pos
        self.frame_num = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if (now - self.last_update) > self.frame_rate:
            self.last_update = now
            self.frame_num += 1
            if self.frame_num == len(self.expl_imgs):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.expl_imgs[self.frame_num]
                self.rect = self.image.get_rect()
                self.rect.center = center
