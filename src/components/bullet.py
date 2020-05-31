"""
This module contains the class for the bullet.
"""
import pygame as pg
import os
import random
from math import atan2, pi, sqrt, cos, sin
from .. import prepare, tools

BULLET_SIZE = (16, 16)
CELL_SIZE = (30, 30)


class Enemy(tools._BaseSprite):
    """
    The class for enemy objects.
    """

    def __init__(self,position, *groups):
        self.pos = [position[0], position[y]]
        x = pos[0]
        y = pos[1]
        tools._BaseSprite.__init__(
            self, (x, y), CELL_SIZE, *groups)
        # self.controls = prepare.DEFAULT_CONTROLS

        self.mask = self.make_mask()
        self.direction = "right"
        self.direction_stack = []
        self.speed = 15
        self.angle = 0
        self.movement = False

        self.bulletImage = pg.image.load(
            os.path.join(os.getcwd(), "src/images/redbullet.png"))
        self.bulletImage = pg.transform.scale(self.bulletImage, (16, 16))
        self.image = self.make_image(self.bulletImage)

    def make_image(self, imageA):
        base = pg.Surface(CELL_SIZE).convert()
        base.fill((255, 255, 255, 0))
        image = base.copy()
        rotatedImage, origin = tools.rotateImage(image, self.bulletImage,
                                                 (23, 23), (16, 16), self.angle)
        image.blit(rotatedImage, origin)
        return image

    def make_mask(self):
        """Create a collision mask for the bullet."""
        temp = pg.Surface(CELL_SIZE).convert_alpha()
        temp.fill((0, 0, 0, 0))
        temp.fill(pg.Color("white"), (10, 20, 30, 30))
        return pg.mask.from_surface(temp)

    def checkOutOfBounds(self):
        right = prepare.SCREEN_SIZE[0] - ((self.rect.width) / 2)
        bottom = prepare.SCREEN_SIZE[1] - (self.rect.height / 2)

        #Have to check this, what we want is if it touches bounds, then delete
        if self.exact_pos[0] < 0 or self.exact_pos[0] > right or \
                self.exact_pos[1] < 0 or self.exact_pos[1] > bottom:
                    return -1
        else:
            pass

    def rot_center(self, image, angle):
        center = image.get_rect().center
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect

    def move(self, playerx, playery, angle):
        """Move the bullet."""
        self.exact_pos[0] += self.speed * cos(angle)
        self.exact_pos[1] += self.speed * sin(angle)

    def update(self, playerx, playery, playerIsMoving, *args):
        """Updates player every frame."""
        self.old_pos = self.exact_pos[:]
        self.move()
        self.checkOutOfBounds()
        self.image = self.make_image(self.bulletImage)
        self.rect.center = self.exact_pos
