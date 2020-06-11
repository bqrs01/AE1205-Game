"""
 File: player.py
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


>>> This module contains the class for the player.
"""
import pygame as pg
import os
import random
from math import atan2, pi, sqrt
from .. import prepare, tools

PLAYER_SIZE = (32, 32)
CELL_SIZE = (46, 46)

SPEED = 10

BULLET_COOLDOWN = 300
BULLET_COOLDOWN_INF = 50
BULLET_COOLDOWN_SAFEZONE = 100

SAFEZONE_TIME = 4000  # ms
EXPLOSION_COOLDOWN = 500

BLINK_COOLDOWN = 150


class Player(tools._BaseSprite):
    """
    The class for player objects. It will be used to keep
    track of scores, health and more.
    """

    def __init__(self, bulletManager, statsManager, explosionManager, *groups):
        tools._BaseSprite.__init__(
            self, prepare.STARTING_POS, CELL_SIZE, *groups)
        self.controls = prepare.DEFAULT_CONTROLS

        self.statsManager = statsManager
        self.bulletManager = bulletManager
        self.explosionManager = explosionManager

        self.direction = "right"
        self.direction_stack = []
        self.speed = SPEED
        self.angle = 0
        self.target_position = (
            prepare.SCREEN_SIZE[0]//2, prepare.SCREEN_SIZE[1]//2)
        self.movement = False
        self.isMoving = False

        self.safe_zone = False
        self.sz_timer = False
        self.sz_time = SAFEZONE_TIME
        self.blink_on = False
        self.blink_cooldown = BLINK_COOLDOWN
        self.expl_cooldown = 0
        self.canPlayerMove = True

        self.bullet_cooldown = BULLET_COOLDOWN

        self.playerImage = pg.image.load(
            os.path.join(os.getcwd(), "src/images/redplain.png")).convert_alpha()
        self.playerImage = pg.transform.scale(self.playerImage, (32, 32))
        self.image = self.make_image(self.playerImage)

    def make_image(self, imageA):
        base = pg.Surface(CELL_SIZE, pg.SRCALPHA).convert()
        base.fill((255, 255, 0))
        base.set_colorkey((255, 255, 0))
        image = base.copy()
        if (self.safe_zone):
            if self.blink_on:
                rotatedImage, origin = tools.rotateImage(image, self.playerImage,
                                                         (23, 23), (16, 16), self.angle)
                image.blit(rotatedImage, origin)
        else:
            rotatedImage, origin = tools.rotateImage(image, self.playerImage,
                                                     (23, 23), (16, 16), self.angle)
            image.blit(rotatedImage, origin)
        return image

    def make_mask(self):
        """Create a collision mask for the player."""
        temp = pg.Surface(CELL_SIZE).convert_alpha()
        temp.fill((0, 0, 0, 0))
        temp.fill(pg.Color("white"), (10, 20, 30, 30))
        return pg.mask.from_surface(temp)

    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in self.controls:
            self.movement = True
            direction = self.controls[key]
            if direction in self.direction_stack:
                self.direction_stack.remove(direction)
            self.direction_stack.append(direction)

    def pop_direction(self, key):
        """Pop a released key from the direction stack."""
        if key in self.controls:
            direction = self.controls[key]
            if direction in self.direction_stack:
                self.direction_stack.remove(direction)

    def checkOutOfBounds(self):
        right = prepare.SCREEN_SIZE[0] - (self.rect.width//2)
        bottom = prepare.SCREEN_SIZE[1] - (self.rect.height//2)
        if self.exact_pos[0] < (self.rect.width//2):
            self.exact_pos[0] = (self.rect.width//2)
        elif self.exact_pos[0] > right:
            self.exact_pos[0] = right

        if self.exact_pos[1] < (self.rect.height//2):
            self.exact_pos[1] = (self.rect.height//2)
        elif self.exact_pos[1] > bottom:
            self.exact_pos[1] = bottom

    def shoot(self):
        """Shoot a bullet."""
        if (self.bullet_cooldown <= 0) or (self.safe_zone):
            self.bulletManager.new(self, 'redbullet')
            self.bullet_cooldown = BULLET_COOLDOWN

    def update_angle(self, position):
        # Gets position of the mouse
        mousex, mousey = position
        # To calculate the angle
        self.angle = atan2(-(mousey - self.rect.center[1]),
                           (mousex - self.rect.center[0])) * 180 / pi - 90

        self.target_position = position

    def got_shot(self):
        """When player gets shot..."""
        if not self.safe_zone:
            self.statsManager.dropHealth(5)
            self.statsManager.reset_powerups()
            self.safe_zone = True
            self.bullet_cooldown = BULLET_COOLDOWN_SAFEZONE
            self.blink_cooldown = BLINK_COOLDOWN
            self.sz_timer = True
            self.sz_time = SAFEZONE_TIME

    def captured(self):
        """When player gets captured..."""
        if not self.safe_zone:
            self.statsManager.dropHealth(10)
            self.statsManager.reset_powerups()
            self.safe_zone = True
            self.bullet_cooldown = BULLET_COOLDOWN_SAFEZONE
            self.blink_cooldown = BLINK_COOLDOWN
            self.canPlayerMove = False
            self.sz_timer = True
            self.sz_time = SAFEZONE_TIME
            self.expl_cooldown = EXPLOSION_COOLDOWN

            self.explosionManager.new_explosion(tuple(self.exact_pos))

    def enemy_shot(self):
        """Increase score when enemy get's shot with player's projectile."""
        if self.safe_zone:
            self.statsManager.addScore(5)
        else:
            self.statsManager.addScore(10)
        self.statsManager.addKill()

    def move(self):
        """Move the player."""
        if self.direction_stack:
            if len(self.direction_stack) == 2:
                con_1 = (
                    'right' in self.direction_stack and 'left' in self.direction_stack)
                con_2 = (
                    'up' in self.direction_stack and 'down' in self.direction_stack)
                if not (con_1 or con_2):
                    vector = [0, 0]
                    for direction in self.direction_stack:
                        vector[0] += prepare.DIRECT_DICT[direction][0]
                        vector[1] += prepare.DIRECT_DICT[direction][1]
                else:
                    vector = [0, 0]
            else:
                self.direction = self.direction_stack[-1]
                vector = prepare.DIRECT_DICT[self.direction]

            self.exact_pos[0] += self.speed*vector[0]
            self.exact_pos[1] += self.speed*vector[1]

    def update(self, dt, *args):
        """Updates player every frame."""
        if self.sz_timer:
            self.sz_time -= dt
            self.blink_cooldown -= dt
            self.expl_cooldown -= dt
            if self.blink_cooldown < 0:
                self.blink_on = not self.blink_on
                self.blink_cooldown = BLINK_COOLDOWN
            if self.expl_cooldown < 0:
                self.canPlayerMove = True
            if self.sz_time < 0:
                self.safe_zone = False
                self.sz_timer = False
                # Safe zone off

        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= dt
        else:
            if self.statsManager.infinity:
                self.shoot()
                self.bullet_cooldown = BULLET_COOLDOWN_INF

        if not (self.old_pos == self.exact_pos):
            self.isMoving = True
        else:
            self.isMoving = False

        self.old_pos = self.exact_pos[:]

        if self.canPlayerMove:
            self.move()
            self.checkOutOfBounds()
            self.image = self.make_image(self.playerImage)
            self.rect.center = self.exact_pos
