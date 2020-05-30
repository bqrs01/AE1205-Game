"""
This module contains the class for the player.
"""
import pygame as pg
from .. import prepare, tools


class Player(tools._BaseSprite):
    """
    The class for player objects. It will be used to keep
    track of scores, health and more.
    """

    def __init__(self, *groups):
        tools._BaseSprite.__init__(
            self, prepare.STARTING_POS, (50, 50), *groups)
        self.controls = prepare.DEFAULT_CONTROLS
        self.image = self.make_image()
        self.mask = self.make_mask()
        self.direction = "right"
        self.direction_stack = []
        self.speed = 8

    def make_image(self):
        base = pg.Surface((50, 50)).convert()
        base.fill((0, 0, 0, 0))
        image = base.copy()
        pg.draw.circle(image, (255, 0, 0), (25, 25), 15)
        return image

    def make_mask(self):
        """Create a collision mask for the player."""
        temp = pg.Surface((50, 50)).convert_alpha()
        temp.fill((0, 0, 0, 0))
        temp.fill(pg.Color("white"), (10, 20, 30, 30))
        return pg.mask.from_surface(temp)

    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in self.controls:
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
        right = prepare.SCREEN_SIZE[0] - self.rect.width
        bottom = prepare.SCREEN_SIZE[1] - self.rect.height
        if self.exact_pos[0] < 0:
            self.exact_pos[0] = 0
        elif self.exact_pos[0] > right:
            self.exact_pos[0] = right

        if self.exact_pos[1] < 0:
            self.exact_pos[1] = 0
        elif self.exact_pos[1] > bottom:
            self.exact_pos[1] = bottom

    def move(self):
        """Move the player."""
        if self.direction_stack:
            print(self.direction_stack)
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
        self.old_pos = self.exact_pos[:]
        self.move()
        self.checkOutOfBounds()
        # print(self.exact_pos)
        self.rect.topleft = self.exact_pos
