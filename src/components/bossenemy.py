"""
 File: bossenemy.py
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


>>> This module contains the class for the boss enemy.
"""
import pygame as pg
import os
import random
from math import atan2, pi, sqrt, cos, sin
from .. import prepare, tools

vec = pg.math.Vector2

ENEMY_SIZE = (64, 64)
CELL_SIZE = (90, 90)
MAX_SPEED = 5
APPROACH_RADIUS = 100
MAX_FORCE = 0.1

NUMBER_BULLETS = 6
SHOOTING_INTERVAL = 1000
TIME_BETWEEN_BULLETS = 50


class BossEnemyManager(pg.sprite.Group):
    def __init__(self, bulletManager):
        super(BossEnemyManager, self).__init__()
        self.bulletManager = bulletManager

    def update(self, player, *args):
        """ Updates all the bossenemies """
        for enemy in self.sprites():
            self.collided(enemy)
            self.checkCollisionWithPlayer(player)
            enemy.update(*args)

    def checkCollisionWithPlayer(self, player):
        """Checks if it collides with the player"""
        if not player.safe_zone:
            collisions = pg.sprite.spritecollide(
                player, self, False)

            if len(collisions) > 0:
                player.captured()
            for enemy in collisions:
                enemy.kill()

    def collided(self, spriteC):
        for sprite in self.sprites():
            if sprite != spriteC and sprite.rect.colliderect(spriteC):
                A_x = sprite.rect.x
                A_y = sprite.rect.y
                B_x = spriteC.rect.x
                B_y = spriteC.rect.y
                A_to_B = vec((B_x - A_x, B_y - A_y))
                A_to_B.rotate_ip(180)
                magnitude = sprite.vel.magnitude()
                if magnitude != 0:
                    try:
                        A_to_B.scale_to_length(magnitude)
                        sprite.pos += A_to_B
                    except Exception:
                        # Do nothing
                        pass

    def generate(self, number=1):
        if not len(self) > 0:
            self.add(BossEnemy(self.bulletManager, self))

    def draw(self, surface):
        for enemy in self.sprites():
            enemy.draw(surface)

    def remove(self, *sprites):
        super(BossEnemyManager, self).remove(*sprites)


class BossEnemy(tools._BaseSprite):
    """
    The class for enemy objects.
    """

    def __init__(self, bulletManager, *groups):
        (x, y) = self.random_pos()

        tools._BaseSprite.__init__(
            self, (x, y), CELL_SIZE, *groups)

        self.bulletManager = bulletManager

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

        self.lives = 10
        self.dead = False

        self.enemyImages = self.generate_images()
        self.image = self.make_image()

        self.shooting_timer = SHOOTING_INTERVAL
        self.time_between_bullets = TIME_BETWEEN_BULLETS
        self.number_bullets = NUMBER_BULLETS
        self.bulletcounter = self.number_bullets

    def generate_images(self):
        images = {}
        for i in range(1, 11):
            image = pg.image.load(
                os.path.join(os.getcwd(), f"src/images/greenplain{i}.png")).convert_alpha()
            image = pg.transform.scale(image, (64, 64))
            images[i] = image
        return images

    def random_pos(self):
        r_x = random.choice([(40, 100), (1100, 1160)])
        r_y = random.choice([(40, 100), (600, 660)])
        x = random.randint(*r_x)
        y = random.randint(*r_y)
        return (x, y)

    def make_image(self):
        base = pg.Surface(CELL_SIZE, pg.SRCALPHA).convert()
        base.fill((255, 255, 0))
        # base.set_alpha(0)
        base.set_colorkey((255, 255, 0))
        image = base.copy()
        rotatedImage, origin = tools.rotateImage(image, self.enemyImages[self.lives],
                                                 (46, 46), (32, 32), self.angle)
        image.blit(rotatedImage, origin)
        return image

    def checkOutOfBounds(self):
        right = prepare.SCREEN_SIZE[0] - ((self.rect.width) / 2)
        bottom = prepare.SCREEN_SIZE[1] - (self.rect.height / 2)
        if self.pos.x < 23:
            self.pos.x = 23
        elif self.pos.x > right:
            self.pos.x = right

        if self.pos.y < 23:
            self.pos.y = 23
        elif self.pos.y > bottom:
            self.pos.y = bottom

    def rot_center(self, image, angle):
        """ Used in order to correctly rotate the image"""
        center = image.get_rect().center
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect

    def update_angle(self, target):
        """Update angle."""
        self.angle = atan2(-(target.y - self.pos.y),
                           (target.x - self.pos.x)) * 180 / pi - 90

    def seek(self, target):
        """Steer towards the player"""
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

    def shoot(self):
        """Intialise a bullet and shoot."""
        self.bulletManager.new(self, 'greenbullet')

    def got_shot(self):
        """Boss got shot by player. Reduce lives."""
        self.lives -= 1
        if self.lives == 0:
            self.dead = True

    def check_collision_isStart(self, s1, s2):
        return s1 != s2 and s1.rect.colliderect(s2.rect)

    def update(self, playerx, playery, playerIsMoving, safe_zone, dt, *args):
        """Updates player every frame."""
        # Set target vector
        self.target = vec(playerx, playery)

        if self.isStart:
            while True:
                pos = vec(self.rect.x, self.rect.y)
                dist = (self.target - pos)

                if dist.magnitude() <= 500:
                    self.rect.x = random.randint(
                        20, prepare.SCREEN_SIZE[0] - 20)
                    self.rect.y = random.randint(
                        20, prepare.SCREEN_SIZE[1] - 20)
                else:
                    break
            self.pos = vec(self.rect.x, self.rect.y)
            self.isStart = False

        # For bullet
        self.target_position = (playerx, playery)

        self.old_pos = self.pos
        self.update_angle(self.target)

        if not safe_zone:
            self.shooting_timer -= dt
            if self.shooting_timer <= 0:
                self.time_between_bullets -= dt
            if self.shooting_timer <= 0 and self.time_between_bullets <= 0 and self.bulletcounter < self.number_bullets:
                self.bulletcounter += 1
                self.shoot()
                self.time_between_bullets = TIME_BETWEEN_BULLETS
            elif self.bulletcounter == self.number_bullets:
                self.bulletcounter = 0
                self.shooting_timer = SHOOTING_INTERVAL

        if not (safe_zone):
            # Update velocity, acceleration and position
            self.move(self.target)

        self.image = self.make_image()
        self.rect.center = self.pos
