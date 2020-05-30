# Im trying this file to try to declare some objects and functions
import pygame as pg
from math import sqrt, atan2, pi, cos, sin


# HERE IM JUST SETTING THE VALUES, I DONT NOW HOW TO ACTUALLY SHOW IT IN THE SCREEN AND APPLY THE CHANGES :)

class Player(object):
    def __init__(self):
        # Position and angle
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.img = pg.image.load("./images/redplain.png")
        self.img = pg.transform.scale(self.img, (32, 32))

    def movement(self, event):
        """Changes movement conditions"""
        if event.type == pg.KEYDOWN:

            # For the speed we can actually do this or do like with the enemy and bullet. If no buttons are touched
            # it can be 0 the speed. But like, max speed being 2, no matter if you press one arrow or two
            if event.key == pg.K_d:
                self.x_vel = 2
            elif event.key == pg.K_a:
                self.x_vel = -2
            elif event.key == pg.K_w:
                self.y_vel = 2
            elif event.key == pg.K_s:
                self.y_vel = -2
            elif event.key == pg.SPACE:  # instead of this key you can set this to a mouseclick
                pass  # Shoot bullet
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.type == pg.K_RIGHT:
                self.x_vel = 0
            if event.key == pg.K_UP or event.type == pg.K_DOWN:
                self.y_vel = 0

    # If you want we can add this to movement
    def rotate(self, event):
        """Rotates player"""
        if event.type == pg.MOUSEMOTION:
            # Gets position of the mouse
            mousex, mousey = event.pos
            # To calculate the angle
            self.angle = atan2(-(mousey - self.y_pos), (mousex - self.x_pos)) * 180 / pi - 90
            # uses -90 in order to point in the direction of the mouse

    def draw(self):
        pass
        """I DONT KNOW HOW YOU HAVE TO DO IT TO DRAW IN THIS CODE, BUT TO DRAW THE OBJECT YOU HAVE TO USE:
        screen.blit(pg.transform.rotate(self.img,self.angle),(self.x_pos,self.y_pos))"""


class Enemy1(object):
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.vel = 2  # we have to do that the velocity modulus is constant, but depending in the position wrt
        # the Player x and y vel variate, always summing a modulus of 2
        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.img = pg.image.load("./images/whiteplain.png")
        self.img = pg.transform.scale(self.img, (32, 32))

    def movement(self, playerx, playery):
        self.angle = atan2(-(playery - self.y_pos), (playerx - self.x_pos)) * 180 / pi
        self.x_vel = cos(self.angle * pi / 180) * self.vel
        self.y_vel = sin(self.angle * pi / 180) * self.vel

    def draw(self):
        """ I dont know how to draw it xD, but the same as before:
        screen.blit(pg.transform.rotate(self.img,self.angle),(self.x_pos,self.y_pos))"""


class Enemy2(object):
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.vel = 2  # we have to do that the velocity modulus is constant, but depending in the position wrt
        # the Player x and y vel variate, always summing a modulus of 2
        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.img = pg.image.load("./images/greenplain.png")
        self.img = pg.transform.scale(self.img, (32, 32))

    def movement(self, playerx, playery):
        self.angle = atan2(-(playery - self.y_pos), (playerx - self.x_pos)) * 180 / pi
        self.x_vel = cos(self.angle * pi / 180) * self.vel
        self.y_vel = sin(self.angle * pi / 180) * self.vel

    def draw(self):
        """ I dont know how to draw it xD, but the same as before:
        screen.blit(pg.transform.rotate(self.img,self.angle),(self.x_pos,self.y_pos))"""


class Bullet(object):
    def __init__(self):
        # Maybe change this to the position of the vehicle
        self.x_pos = 0
        self.y_pos = 0
        self.vel = 2
        self.x_vel = 0
        self.y_vel = 0
        self.img = pg.image.load("")
        self.img = pg.transform.scale(self.img, (16, 16))

    def movement(self, playerx, playery, angle):
        self.x_pos = playerx  # We need to change this so it appears in the middle of the obj in front
        self.y_pos = playery  # Same
        self.x_vel = self.vel * cos(angle)
        self.y_vel = self.vel * sin(angle)
        # We also need to define the impact, or when it reaches the end of the screen

    def draw(self):
        """ We also need to draw this, as
        creen.blit(pg.transform.rotate(self.img,slef.angle),(self.x_pos,self.y_pos))"""
        pass
