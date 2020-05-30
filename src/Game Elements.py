# Im trying this file to try to declare some objects and functions
import pygame as pg
from math import sqrt, atan2, pi


# HERE IM JUST SETTING THE VALUES, I DONT NOW HOW TO ACTUALLY SHOW IT IN THE SCREEN AND APPLY THE CHANGES :)

class Player(object):
    def __init__(self):
        # Position and angle
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.img = pg.image.load("./images/whiteplain.png")
        self.img = pg.transform.scale(self.img, (32, 32))

    def movement(self, event):
        """Changes movement conditions"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.x_vel = 2
            elif event.key == pg.K_a:
                self.x_vel = -2
            elif event.key == pg.K_w:
                self.y_vel = 2
            elif event.key == pg.K_s:
                self.y_vel = -2
            elif event.key == pg.SPACE:
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
        screen.blit(pg.transform.rotate(self.img,slef.angle),(self.x_pos,self.y_pos))"""
class Enemy(object):
    def __init__(self):
