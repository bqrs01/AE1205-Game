"""
This module contains the class for the bullet.
"""
import pygame as pg
import os
import random
from math import atan2, pi, sqrt, cos, sin
from .. import prepare, tools

BULLET_SIZE = (32, 32)
CELL_SIZE = (46, 46)


class BulletManager(pg.sprite.Group):
    def __init__(self):
        super(BulletManager, self).__init__()
        # self.enemy_objects = []

    def add(self, *sprites):
        super().add(*sprites)

    def update(self, *args):
        for bullet in self.sprites():
            bullet.update(*args)
            self.collided(bullet)

    def collided(self, spriteC):
        for sprite in self.sprites():
            if sprite != spriteC and sprite.rect.colliderect(spriteC):
                A_x = sprite.rect.x
                A_y = sprite.rect.y
                B_x = spriteC.rect.x
                B_y = spriteC.rect.y
                A_to_B = atan2(B_y-A_y, B_x-A_x)
                reverse = tools.Vector(
                    30, tools.Vector.getReverseDirection(A_to_B))
                sprite.exact_pos = [
                    A_x + reverse.getComponents()[0], A_y + reverse.getComponents()[1]]

    def new(self, owner):
        print(owner)
        self.add(Bullet(owner))

    def draw(self, surface):
        for bullet in self.sprites():
            bullet.draw(surface)

    def remove(self, *sprites):
        super(BulletManager, self).remove(*sprites)
        # for sprite in sprites:
        #     self.enemy_objects.remove(sprite)


class Bullet(tools._BaseSprite):
    """
    The class for enemy objects.
    """

    def __init__(self, owner, *groups):
        self.owner = owner
        position = (self.owner.rect.centerx, self.owner.rect.centery)
        self.pos = [position[0], position[1]]
        x = self.pos[0]
        y = self.pos[1]

        tools._BaseSprite.__init__(
            self, (x, y), CELL_SIZE, *groups)
        # self.controls = prepare.DEFAULT_CONTROLS

        self.mask = self.make_mask()
        self.direction = "right"
        self.direction_stack = []
        self.speed = 15

        mouse_position = self.owner.mouse_position

        dis = tools.Vector(
            self.speed, atan2(-(mouse_position[1]-y), (mouse_position[0]-x)))

        self.angle = (dis.direction * 180/pi) - 90
        self.angle2 = (dis.direction * 180/pi)
        self.movement = False

        self.bulletImage = pg.image.load(
            os.path.join(os.getcwd(), "src/images/redbullet.png"))
        self.bulletImage = pg.transform.scale(self.bulletImage, (32, 32))
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

        # Have to check this, what we want is if it touches bounds, then delete
        if self.exact_pos[0] < 0 or self.exact_pos[0] > right or \
                self.exact_pos[1] < 0 or self.exact_pos[1] > bottom:
            self.remove()
            return -1
        else:
            pass

    # def rot_center(self, image, angle):
    #     self.angle = angle
    #     center = image.get_rect().center
    #     rotated_image = pg.transform.rotate(image, angle)
    #     new_rect = rotated_image.get_rect(center=center)
    #     return rotated_image, new_rect

    def move(self):
        """Move the bullet."""
        #vector = tools.Vector(self.speed, self.angle * pi/180)
        # print(self.angle)
        #self.speed * cos(self.angle * pi/180)
        self.exact_pos[0] += self.speed * \
            cos(self.angle2 * pi/180)  # vector.getComponents()[0]
        self.exact_pos[1] += self.speed * \
            -sin(self.angle2 * pi/180)  # vector.getComponents()[1]

    def update(self, *args):
        """Updates player every frame."""
        self.old_pos = self.exact_pos[:]
        self.move()
        self.checkOutOfBounds()
        self.rect.center = self.exact_pos
