"""
 File: tutorial_screen.py
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
"""

import sys
import os
import pygame as pg

from .. import tools, prepare

# Intro screen


class TutorialScreen(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(TutorialScreen, self).__init__()
        self.images = {}
        self.imageFilenames = ['tutorial1',
                               'tutorial2', 'tutorial3']
        self.gen_images()
        self.imageTimes = [8000, 18000, 4000]
        self.image = self.images[0]['frames'][0]
        self.rect = self.image.get_rect(center=prepare.SCREEN_CENTER)
        self.frame_num = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 70
        self.loading = True
        self.image_num = 0
        # Set next state
        self.next_state = "MAINSCREEN"

        self.intro = {}

    def startup(self, game_data):
        self.frame_num = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 70
        self.loading = True
        self.image_num = 0
        self.next_state = "MAINSCREEN"
        self.image = self.images[0]['frames'][0]

    def gen_images(self):
        for idx1 in range(len(self.imageFilenames)):
            images = []
            for idx2 in range(17):
                image = pg.image.load(os.path.join(
                    os.getcwd(), f"src/images/{self.imageFilenames[idx1]}.png")).convert()
                image.set_alpha((idx2+1)*15)
                images.append(image)
            self.images[idx1] = {"frames": images}

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if self.intro['get_done']():
                    self.done = True

    def next_image(self):
        self.image_num += 1
        if self.image_num >= len(self.imageFilenames):
            # Stop
            self.intro['set_done'](newValue=True)
            self.done = True
        else:
            self.last_update = pg.time.get_ticks()
            self.loading = True
            self.image = self.images[self.image_num]['frames'][0]
            self.frame_num = 0

    def update(self, dt):
        if self.loading:
            now = pg.time.get_ticks()
            if (now - self.last_update) > self.frame_rate:
                self.last_update = now
                self.frame_num += 1
                if self.frame_num == len(self.images[self.image_num]['frames']):
                    self.loading = False
                else:
                    self.image = self.images[self.image_num]["frames"][self.frame_num]
                    self.rect = self.image.get_rect()
                    self.rect.center = prepare.SCREEN_CENTER
        else:
            now = pg.time.get_ticks()
            if (now - self.last_update) > self.imageTimes[self.image_num]:
                # Next picture
                self.next_image()

    def draw(self, surface):
        if self.loading:
            surface.fill((0, 0, 0, (self.frame_num+1)*15))
        else:
            surface.fill((0, 0, 0))

        surface.blit(self.image, self.rect)
