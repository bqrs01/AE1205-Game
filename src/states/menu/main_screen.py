"""
 File: main_screen.py
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


class MainScreen(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(MainScreen, self).__init__()
        # self.images = []
        # self.gen_images()
        self.image = pg.image.load(os.path.join(
            os.getcwd(), "src/images/mainscreenbg.png")).convert()
        self.rect = self.image.get_rect(center=prepare.SCREEN_CENTER)

        # Set next state
        self.next_state = "GAMEPLAY"

        self.logo = pg.image.load(os.path.join(
            os.getcwd(), "src/images/Firecraze.png")).convert_alpha()
        self.logo.set_colorkey((0, 0, 0))
        self.logo_rect = self.logo.get_rect(
            center=(prepare.SCREEN_CENTER[0], 110))

        self.mousepos = (0, 0)

        self.button_names = ["playbutton", "controlsbutton", "settingbutton"]
        self.button_pos = [260, 380, 500]
        self.button_size = [(300, 90), (300, 90), (300, 90)]
        self.button_states = ["GAMEPLAY", "CONTROLS", "SETTINGS"]
        self.buttons = []
        self.buttons_focused = []
        self.buttons_rects = []
        self.focused_button = -1

        self.get_button_images()

        self.play_button = pg.image.load(os.path.join(
            os.getcwd(), "src/images/playbutton_unfocused.png")).convert_alpha()
        self.play_button = pg.transform.scale(self.play_button, (300, 90))
        self.play_button_rect = self.play_button.get_rect(
            center=(prepare.SCREEN_CENTER[0], 200))

        self.bgmusic = {}

        self.sub_font = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 35)
        self.copyright = self.sub_font.render(
            "Copyright (c) 2020 Mario Padrón Tardáguila & Bryan Quadras", True, pg.color.Color('yellow'))
        self.copyright_rect = self.copyright.get_rect(center=(600, 615))

        self.sub_font_2 = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 18)

    def get_button_images(self):
        for i, name in enumerate(self.button_names):
            button = pg.image.load(os.path.join(
                os.getcwd(), f"src/images/{name}_unfocused.png")).convert_alpha()
            button = pg.transform.scale(button, self.button_size[i])
            button_rect = button.get_rect(
                center=(prepare.SCREEN_CENTER[0], self.button_pos[i]))
            self.buttons.append(button)
            self.buttons_rects.append(button_rect)

            f_button = pg.image.load(os.path.join(
                os.getcwd(), f"src/images/{name}_focused.png")).convert_alpha()
            f_button = pg.transform.scale(f_button, self.button_size[i])
            self.buttons_focused.append(f_button)

    def draw_buttons(self, surface):
        for i, button in enumerate(self.buttons):
            if self.focused_button == i:
                surface.blit(self.buttons_focused[i], self.buttons_rects[i])
            else:
                surface.blit(button, self.buttons_rects[i])

    def button_selected(self):
        if self.focused_button != -1:
            self.next_state = self.button_states[self.focused_button]
            self.done = True

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        # elif event.type == pg.KEYDOWN:
        #     if event.key == pg.K_SPACE:
        #         self.done = True
        elif event.type == pg.MOUSEMOTION:
            self.mousepos = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            self.button_selected()

    def startup(self, game_data):
        self.current_song = self.sub_font_2.render(
            f"Song: {self.bgmusic['song_name']}", True, pg.color.Color('green'))
        self.current_song_rect = self.current_song.get_rect(
            center=(600, 665))
        self.focused_button = -1
        self.mousepos = (0, 0)

    def check_if_focused(self):
        focus_happened = False
        for idx in range(len(self.buttons)):
            x = self.mousepos[0]
            y = self.mousepos[1]
            button_rect = self.buttons_rects[idx]
            if button_rect.collidepoint(x, y):
                # Button is focused.
                self.focused_button = idx
                focus_happened = True
                break
        if not focus_happened:
            self.focused_button = -1

    def update(self, dt):
        self.current_song = self.sub_font_2.render(
            f"Song: {self.bgmusic['song_name']}", True, pg.color.Color('green'))
        self.current_song_rect = self.current_song.get_rect(
            center=(600, 665))
        self.check_if_focused()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.logo, self.logo_rect)
        surface.blit(self.copyright, self.copyright_rect)
        surface.blit(self.current_song, self.current_song_rect)
        #surface.blit(self.play_button, self.play_button_rect)
        self.draw_buttons(surface)
