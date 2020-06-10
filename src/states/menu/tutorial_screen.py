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


class TutorialScreen(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(TutorialScreen, self).__init__()
        # self.images = []
        # self.gen_images()
        self.image = pg.image.load(os.path.join(
            os.getcwd(), "src/images/keyboard.png")).convert()
        self.rect = self.image.get_rect(center=prepare.SCREEN_CENTER)
        # Set next state
        self.next_state = "MAINSCREEN"

        self.logo = pg.image.load(os.path.join(
            os.getcwd(), "src/images/Firecraze.png")).convert_alpha()
        self.logo.set_colorkey((0, 0, 0))
        self.logo_rect = self.logo.get_rect(
            center=(prepare.SCREEN_CENTER[0], 110))

        # self.sub_font = pg.font.Font(os.path.join(
        #     os.getcwd(), "src/fonts/FORTE.TTF"), 35)
        # self.go_back = self.sub_font.render(
        #     "Press ESC to go back", True, pg.color.Color("green"))
        # self.go_back_rect = self.go_back.get_rect(topleft=(85, 625))

        self.focused_button = False

        self.button = pg.image.load(os.path.join(
            os.getcwd(), "src/images/arrowbutton_unfocused.png")).convert_alpha()
        # self.button = pg.transform.scale(button, (40, 20))
        self.button_rect = self.button.get_rect(
            center=(40, 40))

        self.f_button = pg.image.load(os.path.join(
            os.getcwd(), "src/images/arrowbutton_focused.png")).convert_alpha()
        # self.f_button = pg.transform.scale(self.f_button, self.button_size[i])

        self.mousepos = (0, 0)

    def draw_buttons(self, surface):
        if self.focused_button:
            surface.blit(self.f_button, self.button_rect)
        else:
            surface.blit(self.button, self.button_rect)

    def button_selected(self):
        if self.focused_button:
            self.next_state = "MAINSCREEN"
            self.done = True

    def check_if_focused(self):
        x = self.mousepos[0]
        y = self.mousepos[1]
        button_rect = self.button_rect
        if button_rect.collidepoint(x, y):
            # Button is focused.
            self.focused_button = True
        else:
            self.focused_button = False

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.button_selected()
            # if event.key == pg.K_ESCAPE:
            #     self.done = True
        elif event.type == pg.MOUSEMOTION:
            self.mousepos = event.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # surface.blit(self.go_back, self.go_back_rect)
        self.draw_buttons(surface)

    def update(self, dt):
        self.check_if_focused()
