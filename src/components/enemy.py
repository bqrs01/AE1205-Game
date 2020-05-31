"""
This module contains the class for the enemy.
"""
import pygame as pg
import os
from math import atan2, pi, sqrt, cos, sin
from .. import prepare, tools

ENEMY_SIZE = (32, 32)
CELL_SIZE = (46, 46)


class Enemy(tools._BaseSprite):
    """
    The class for enemy objects.
    """

    def __init__(self, *groups):
        tools._BaseSprite.__init__(
            self, prepare.STARTING_POS, CELL_SIZE, *groups)
        # self.controls = prepare.DEFAULT_CONTROLS

        self.mask = self.make_mask()
        self.direction = "right"
        self.direction_stack = []
        self.speed = 2
        self.angle = 0
        self.movement = False

        self.enemyImage = pg.image.load(
            os.path.join(os.getcwd(), "src/images/whiteplain3.png"))
        self.enemyImage = pg.transform.scale(self.enemyImage, (32, 32))
        self.image = self.make_image(self.enemyImage)

    def make_image(self, imageA):
        base = pg.Surface(CELL_SIZE).convert()
        base.fill((255, 255, 255, 0))
        image = base.copy()
        rotatedImage, origin = tools.rotateImage(image, self.enemyImage,
                                                 (23, 23), (16, 16), self.angle)
        image.blit(rotatedImage, origin)
        return image

    def make_mask(self):
        """Create a collision mask for the enemy."""
        temp = pg.Surface(CELL_SIZE).convert_alpha()
        temp.fill((0, 0, 0, 0))
        temp.fill(pg.Color("white"), (10, 20, 30, 30))
        return pg.mask.from_surface(temp)

    def checkOutOfBounds(self):
        right = prepare.SCREEN_SIZE[0] - ((self.rect.width) / 2)
        bottom = prepare.SCREEN_SIZE[1] - (self.rect.height / 2)
        if self.exact_pos[0] < 0:
            self.exact_pos[0] = 0
        elif self.exact_pos[0] > right:
            self.exact_pos[0] = right

        if self.exact_pos[1] < 0:
            self.exact_pos[1] = 0
        elif self.exact_pos[1] > bottom:
            self.exact_pos[1] = bottom

    def update_angle(self, position):
        # Gets position of the mouse
        playerx, playery = position
        # To calculate the angle
        self.angle = atan2(-(playerx -
                             self.rect.center[1]), (playery - self.rect.center[0])) * 180 / pi

    def rot_center(self, image, angle):
        center = image.get_rect().center
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect

    def move(self, playerx, playery):
        """Move the enemy."""
        self.angle = atan2(-(playery - self.exact_pos[1]),
                           (playerx - self.exact_pos[0])) * 180 / pi - 90
        self.exact_pos[0] -= self.speed * cos(self.angle)
        self.exact_pos[1] += self.speed * sin(self.angle)

    def update(self, playerx, playery, playerIsMoving, *args):
        """Updates player every frame."""
        if playerIsMoving:
            print("Player moving")
            # self.old_pos = self.exact_pos[:]
            # self.move(playerx, playery)
            # self.checkOutOfBounds()
            # self.image = self.make_image(self.enemyImage)
            # self.rect.center = self.exact_pos
        else:
            print("Player not moving")
            self.old_pos = self.exact_pos[:]
            self.move(playerx, playery)
            self.checkOutOfBounds()
            self.image = self.make_image(self.enemyImage)
            self.rect.center = self.exact_pos
