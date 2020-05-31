"""
This module contains the class for the player.
"""
import pygame as pg
import os
from math import atan2, pi, sqrt
from .. import prepare, tools

PLAYER_SIZE = (32, 32)
CELL_SIZE = (46, 46)


class Player(tools._BaseSprite):
    """
    The class for player objects. It will be used to keep
    track of scores, health and more.
    """

    def __init__(self, *groups):
        tools._BaseSprite.__init__(
            self, prepare.STARTING_POS, CELL_SIZE, *groups)
        self.controls = prepare.DEFAULT_CONTROLS

        self.mask = self.make_mask()
        self.direction = "right"
        self.direction_stack = []
        self.speed = 8
        self.angle = 0
        self.mouse_position = (
            prepare.SCREEN_SIZE[0]//2, prepare.SCREEN_SIZE[1]//2)
        self.movement = False
        self.isMoving = False

        self.playerImage = pg.image.load(
            os.path.join(os.getcwd(), "src/images/redplain.png"))
        self.playerImage = pg.transform.scale(self.playerImage, (32, 32))
        self.image = self.make_image(self.playerImage)

    def make_image(self, imageA):
        base = pg.Surface(CELL_SIZE).convert()
        base.fill((255, 255, 255, 0))
        image = base.copy()
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
        right = prepare.SCREEN_SIZE[0] - ((self.rect.width)/2)
        bottom = prepare.SCREEN_SIZE[1] - (self.rect.height/2)
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
        mousex, mousey = position
        # To calculate the angle
        self.angle = atan2(-(mousey - self.rect.center[1]),
                           (mousex - self.rect.center[0])) * 180 / pi - 90

        self.mouse_position = position

    def rot_center(self, image, angle):
        center = image.get_rect().center
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect

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

    def update(self, *args):
        """Updates player every frame."""
        if not (self.old_pos == self.exact_pos):
            self.isMoving = True
        else:
            self.isMoving = False
        self.old_pos = self.exact_pos[:]
        self.move()
        self.checkOutOfBounds()
        self.image = self.make_image(self.playerImage)
        self.rect.center = self.exact_pos
