"""
 File: settings.py
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


class SettingsScreen(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(SettingsScreen, self).__init__()
        # self.images = []
        # self.gen_images()
        self.image = pg.image.load(os.path.join(
            os.getcwd(), "src/images/mainscreenbg.png")).convert()
        self.rect = self.image.get_rect(center=prepare.SCREEN_CENTER)
        # Set next state
        self.next_state = "MAINSCREEN"

        self.logo = pg.image.load(os.path.join(
            os.getcwd(), "src/images/Firecraze.png")).convert_alpha()
        self.logo.set_colorkey((0, 0, 0))
        self.logo_rect = self.logo.get_rect(
            center=(prepare.SCREEN_CENTER[0], 280))

        self.sub_font = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 50)
        self.sub_font_2 = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 35)

        self.settings = self.sub_font.render(
            "SETTINGS", True, pg.color.Color("green"))
        self.settings_rect = self.settings.get_rect(
            center=(prepare.SCREEN_CENTER[0], 240))

        self.music_lbl = self.sub_font_2.render(
            "MUSIC: ", True, pg.color.Color("yellow"))
        self.music_lbl_rect = self.music_lbl.get_rect(
            topleft=(400, 300))

        self.sfx_lbl = self.sub_font_2.render(
            "SFX: ", True, pg.color.Color("yellow"))
        self.sfx_lbl_rect = self.sfx_lbl.get_rect(
            topleft=(400, 370))

        self.focused_button = False

        self.button = pg.image.load(os.path.join(
            os.getcwd(), "src/images/arrowbutton_unfocused.png")).convert_alpha()
        # self.button = pg.transform.scale(button, (40, 20))
        self.button_rect = self.button.get_rect(
            center=(40, 40))

        self.f_button = pg.image.load(os.path.join(
            os.getcwd(), "src/images/arrowbutton_focused.png")).convert_alpha()
        # self.f_button = pg.transform.scale(self.f_button, self.button_size[i])

        self.bgmusic = {}

        # self.startup()

    def startup(self, game_data):
        self.mousepos = (0, 0)

        self.music_vol = self.bgmusic['get_volume']()
        self.sfx_vol = self.bgmusic['get_sfx_volume']()

        slider_music = tools.Slider(
            self.music_vol, (600, 310), self.on_music_change)
        slider_sfx = tools.Slider(self.sfx_vol, (600, 380), self.on_sfx_change)

        self.sliders = [slider_music, slider_sfx]
        self.focused_slider = -1
        self.isMouseDown = False

    def on_music_change(self, new_value):
        # print("MUSIC", new_value)
        self.bgmusic['set_volume'](new_value)
        self.bgmusic['save_volume']()

    def on_sfx_change(self, new_value):
        self.bgmusic['set_sfx_volume'](new_value)
        self.bgmusic['save_volume']()

    def draw_buttons(self, surface):
        if self.focused_button:
            surface.blit(self.f_button, self.button_rect)
        else:
            surface.blit(self.button, self.button_rect)

    def button_selected(self):
        if self.focused_button:
            # Saves volume
            self.bgmusic['save_volume']()
            self.next_state = "MAINSCREEN"
            self.done = True

    def check_if_button_focused(self):
        x = self.mousepos[0]
        y = self.mousepos[1]
        button_rect = self.button_rect
        if button_rect.collidepoint(x, y):
            # Button is focused.
            self.focused_button = True
        else:
            self.focused_button = False

    def check_if_sliders_focused(self):
        focus_happened = False
        for idx, slider in enumerate(self.sliders):
            x = self.mousepos[0]
            y = self.mousepos[1]
            if slider.rect.collidepoint(x, y):
                self.focused_slider = idx
                focus_happened = True
                break
        if not focus_happened:
            self.focused_slider = -1

    def slider_selected(self):
        if self.focused_slider != -1 and self.isMouseDown:
            self.sliders[self.focused_slider].handle_mouse(self.mousepos)

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.isMouseDown = True
            self.slider_selected()
            pass
        elif event.type == pg.MOUSEBUTTONUP:
            self.button_selected()
            self.isMouseDown = False
            # if event.key == pg.K_ESCAPE:
            #     self.done = True
        elif event.type == pg.MOUSEMOTION:
            self.mousepos = event.pos
            self.slider_selected()

    def draw_sliders(self, surface):
        for slider in self.sliders:
            slider.draw(surface)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.settings, self.settings_rect)
        surface.blit(self.music_lbl, self.music_lbl_rect)
        surface.blit(self.sfx_lbl, self.sfx_lbl_rect)
        self.draw_buttons(surface)
        self.draw_sliders(surface)

    def update(self, dt):
        self.check_if_button_focused()
        self.check_if_sliders_focused()
