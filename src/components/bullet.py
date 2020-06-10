"""
 File: bullet.py
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
 

>>> This module contains the class for the bullet.
"""

import pygame as pg
import os
import random
from math import atan2, pi, sqrt, cos, sin
from .. import prepare, tools
from . import enemy, player, bossenemy

BULLET_SIZE = (32, 32)
CELL_SIZE = (46, 46)

POWERUP_CHANCE = 0.08
HEALTH_CHANCE = 0.50


class BulletManager(pg.sprite.Group):
    def __init__(self, soundManager, powerupManager):
        super(BulletManager, self).__init__()
        self.bulletImages = {}
        self.soundManager = soundManager
        self.powerupManager = powerupManager

    def load_image(self, colour):
        if colour in self.bulletImages.keys():
            return self.bulletImages[colour]
        else:
            image = pg.image.load(
                os.path.join(os.getcwd(), f"src/images/{colour}.png")).convert_alpha()
            self.bulletImages[colour] = image
            return image

    def add(self, *sprites):
        super().add(*sprites)

    def update(self, player, enemyManager, bossenemyManager, explosionManager, *args):
        """Update function for bullet manager."""
        for bullet in self.sprites():
            bullet.update(*args)

        self.checkCollisionWithPlayer(player)
        self.checkCollisionWithEnemy(enemyManager, explosionManager, player)
        self.checkCollisionWithBossEnemy(
            bossenemyManager, explosionManager, player)

    def checkCollisionWithPlayer(self, player):
        """Check bullet collison with player."""
        collisions = pg.sprite.spritecollide(
            player, self, False)

        for bullet in collisions:
            c_with_pl = pg.sprite.collide_rect(player, bullet)
            if not (c_with_pl and bullet.owner == player):
                bullet.kill()
                player.got_shot()

    def checkCollisionWithEnemy(self, enemyManager, explosionManager, player):
        """Check bullet collison with enemy."""
        collisions = pg.sprite.groupcollide(self, enemyManager, False, False)
        for bullet in collisions:
            enemyCollided = collisions[bullet]
            if not (type(bullet.owner) == enemy.Enemy or type(bullet.owner) == bossenemy.BossEnemy):
                bullet.kill()
                # Player shot enemy successfully
                enemyPos = enemyCollided[0].pos
                explosionManager.new_explosion((enemyPos.x, enemyPos.y))
                enemyCollided[0].kill()
                player.enemy_shot()
                # Randomly decide if powerup should appear
                if (random.random() <= POWERUP_CHANCE):
                    self.powerupManager.new_powerup(
                        enemyPos, self.soundManager)

    def checkCollisionWithBossEnemy(self, enemyManager, explosionManager, player):
        """Check bullet collison with boss enemy."""
        collisions = pg.sprite.groupcollide(self, enemyManager, False, False)
        for bullet in collisions:
            enemyCollided = collisions[bullet]
            if not (type(bullet.owner) == bossenemy.BossEnemy or type(bullet.owner) == enemy.Enemy):
                bullet.kill()
                # Player shot boss enemy successfully. So reduce lives by 1.
                enemyCollided[0].got_shot()
                if enemyCollided[0].dead:
                    enemyPos = enemyCollided[0].pos
                    explosionManager.new_explosion((enemyPos.x, enemyPos.y))
                    enemyCollided[0].kill()

                    # Randomly decide if powerup should appear
                    if (random.random() <= HEALTH_CHANCE):
                        self.powerupManager.new_powerup(
                            enemyPos, self.soundManager, health=True)

                player.enemy_shot()

    def new(self, owner, colour):
        image = self.load_image(colour)
        self.add(Bullet(owner, image))
        if type(owner) == player.Player:
            self.soundManager.playSound('laser.wav', duration=225)

    def draw(self, surface):
        for bullet in self.sprites():
            bullet.draw(surface)

    def remove(self, *sprites):
        super(BulletManager, self).remove(*sprites)


class Bullet(tools._BaseSprite):
    """
    The class for enemy objects.
    """

    def __init__(self, owner, image, *groups):
        self.owner = owner
        position = (self.owner.rect.centerx, self.owner.rect.centery)
        self.pos = [position[0], position[1]]
        x = self.pos[0]
        y = self.pos[1]

        tools._BaseSprite.__init__(
            self, (x, y), CELL_SIZE, *groups)

        self.mask = self.make_mask()
        self.direction = "right"
        self.direction_stack = []
        self.speed = 15

        target_position = self.owner.target_position

        dis = tools.Vector(
            self.speed, atan2(-(target_position[1] - y), (target_position[0] - x)))

        self.angle = (dis.direction * 180 / pi) - 90  # For image creation
        self.angle2 = (dis.direction * 180 / pi)  # For movement
        self.movement = False

        self.bulletImage = pg.transform.scale(image, (32, 32))
        self.image = self.make_image(self.bulletImage)

    def make_image(self, imageA):
        """Make image for blitting."""
        base = pg.Surface(CELL_SIZE).convert()
        base.fill((255, 255, 0))
        base.set_colorkey((255, 255, 0))
        image = base.copy()
        rotatedImage, origin = tools.rotateImage(image, self.bulletImage,
                                                 (23, 23), (16, 16), self.angle)
        image.blit(rotatedImage, origin)
        return image

    # def make_mask(self):
    #     """Create a collision mask for the bullet."""
    #     temp = pg.Surface(CELL_SIZE).convert_alpha()
    #     temp.fill((0, 0, 0, 0))
    #     temp.fill(pg.Color("white"), (10, 20, 30, 30))
    #     return pg.mask.from_surface(temp)

    def checkOutOfBounds(self):
        """Check if bullet is out of window."""
        right = prepare.SCREEN_SIZE[0] - ((self.rect.width) / 2)
        bottom = prepare.SCREEN_SIZE[1] - (self.rect.height / 2)

        # Have to check this, what we want is if it touches bounds, then delete
        if self.exact_pos[0] < 0 or self.exact_pos[0] > right or \
                self.exact_pos[1] < 0 or self.exact_pos[1] > bottom:
            self.remove()  # Removes bullet if touches boundary
            return -1
        else:
            pass

    def move(self):
        """Move the bullet."""
        self.exact_pos[0] += self.speed * \
            cos(self.angle2 * pi / 180)
        self.exact_pos[1] += self.speed * \
            -sin(self.angle2 * pi / 180)

    def update(self, *args):
        """Updates player every frame."""
        self.old_pos = self.exact_pos[:]
        self.move()
        self.checkOutOfBounds()
        self.rect.center = self.exact_pos
