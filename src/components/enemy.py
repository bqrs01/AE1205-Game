"""
This module contains the class for the enemy.
"""
import pygame as pg
import os
import random
from math import atan2, pi, sqrt, cos, sin
from .. import prepare, tools

vec = pg.math.Vector2

ENEMY_SIZE = (32, 32)
CELL_SIZE = (46, 46)
MAX_SPEED = 5
APPROACH_RADIUS = 150
MAX_FORCE = 0.1


class EnemyManager(pg.sprite.Group):
    def __init__(self, bulletManager):
        super(EnemyManager, self).__init__()
        # self.enemy_objects = []
        self.bulletManager = bulletManager

    def add(self, *sprites):
        super().add(*sprites)

    def update(self, *args):
        for enemy in self.sprites():
            enemy.update(*args)
            self.collided(enemy)

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

    def generate(self, number=1):
        if len(self) <= 10:
            for _ in range(number):
                self.add(Enemy(self.bulletManager))

    def draw(self, surface):
        for enemy in self.sprites():
            enemy.draw(surface)

    def remove(self, *sprites):
        super(EnemyManager, self).remove(*sprites)
        # for sprite in sprites:
        #     self.enemy_objects.remove(sprite)


class Enemy(tools._BaseSprite):
    """
    The class for enemy objects.
    """

    def __init__(self, bulletManager, *groups):
        x = random.randint(20, prepare.SCREEN_SIZE[0] - 20)
        y = random.randint(20, prepare.SCREEN_SIZE[1] - 20)

        tools._BaseSprite.__init__(
            self, (x, y), CELL_SIZE, *groups)
        # self.controls = prepare.DEFAULT_CONTROLS

        self.bulletManager = bulletManager
        self.mask = self.make_mask()
        self.direction = "right"
        self.direction_stack = []

        self.pos = vec(x, y)
        self.vel = vec(MAX_SPEED, 0).rotate(random.uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.angle = 0
        self.movement = False

        self.isStart = True

        self.target_position = (x, y)

        self.target_position_t = (x, y)
        self.capture_position_now = False
        self.capture_position_time = 0

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
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > right:
            self.pos.x = right

        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > bottom:
            self.pos.y = bottom

    # def update_angle(self, position):
    #     # Gets position of the mouse
    #     playerx, playery = position
    #     # To calculate the angle
    #     self.angle = atan2(-(playerx -
    #                          self.rect.center[1]), (playery - self.rect.center[0])) * 180 / pi

    def rot_center(self, image, angle):
        center = image.get_rect().center
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect

    def update_angle(self, target):
        """Update angle."""
        self.angle = atan2(-(target.y - self.pos.y),
                           (target.x - self.pos.x)) * 180 / pi - 90

    def seek(self, target):
        self.desired = (target - self.pos)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= (dist / APPROACH_RADIUS) * MAX_SPEED
        else:
            self.desired *= MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def move(self, target):
        """Move the enemy."""
        self.acc = self.seek(target)
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        self.checkOutOfBounds()
        self.rect.center = self.pos
        # dist = (target - self.exact_pos).magnitude()
        # if not (dist <= 125):
        #     self.exact_pos[0] -= self.speed * cos(self.angle)
        #     self.exact_pos[1] += self.speed * sin(self.angle)

    def shoot(self):
        """Intialise a bullet and shoot."""
        self.bulletManager.new(self, 'blackbullet')

    def update(self, playerx, playery, playerIsMoving, safe_zone, dt, *args):
        """Updates player every frame."""
        # Set target vector
        self.target = vec(playerx, playery)

        if self.isStart:
            # Check if enemy is close to player
            while True:
                pos = vec(self.rect.x, self.rect.y)
                dist = (self.target-pos)
                if dist.magnitude() <= 125:
                    self.rect.x = random.randint(
                        20, prepare.SCREEN_SIZE[0] - 20)
                    self.rect.y = random.randint(
                        20, prepare.SCREEN_SIZE[1] - 20)
                else:
                    break
            self.pos = vec(self.rect.x, self.rect.y)
            self.isStart = False

        #self.target_position = (playerx, playery)

        # Randomly decide to shoot
        rn = random.randint(1, 1000)
        if rn == 57:
            if not safe_zone:
                self.shoot()

        self.old_pos = self.pos
        self.update_angle(self.target)
        if not (safe_zone):
            # Update velocity, acceleration and position
            self.move(self.target)

        # self.checkOutOfBounds()
        self.image = self.make_image(self.enemyImage)
        self.rect.center = self.pos
