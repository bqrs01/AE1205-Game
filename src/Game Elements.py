# Im trying this file to try to declare some objects and functions
import pygame as pg
from math import sqrt, atan


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

    def movement(self, event):
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

    def rotate(self, event):
        if event.type == pg.MOUSEMOTION:
            mousex, mousey = event.pos
            direction_vector = (mousex - self.x_pos, mousey - self.y_pos)
            angle = atan(direction_vector[1] / direction_vector[0])

