# Im trying this file to try to declare some objects and functions
import pygame as pg


class Player(object):
    def __init__(self):
        # Position and angle
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.img = pg.image.load("./images/whiteplain.png")

