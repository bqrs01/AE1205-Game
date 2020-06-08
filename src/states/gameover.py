"""
 File: gameover.py
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


class GameOver(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(GameOver, self).__init__()
        # Set next state
        self.next_state = "MAINSCREEN"

        self.mousepos = (0, 0)

        self.button_names = ["menubutton"]
        self.button_pos = [430]
        self.button_size = [(180, 54)]
        self.button_states = ["MAINSCREEN"]
        self.buttons = []
        self.buttons_focused = []
        self.buttons_rects = []
        self.focused_button = -1

        self.get_button_images()

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

    def startup(self, game_data):
        self.soundManager = tools.SoundManager('prefs.json')

        self.font_forte_med = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 35)
        self.font_forte_large = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 50)

        self.game_surface = game_data['game_screen']

        self.dim_screen = pg.Surface(prepare.SCREEN_SIZE).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # Set title
        self.title = self.font_forte_large.render(
            "Game Over!", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(
            center=(self.screen_rect.center[0], self.screen_rect.center[1]-45))

        self.subtitle = self.font_forte_med.render(
            f"You got a score of {game_data['final_score']}", True, pg.Color('darkgreen'))
        self.subtitle_rect = self.subtitle.get_rect(
            center=(self.screen_rect.center[0], self.screen_rect.center[1]))

        self.soundManager.playSound('GameOver.mp3', duration=3000)

        self.mousepos = (0, 0)

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEMOTION:
            self.mousepos = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            self.button_selected()

    def update(self, dt):
        self.check_if_focused()

    def draw(self, surface):
        surface.blit(self.game_surface,
                     self.game_surface.get_rect(topleft=(0, 0)))
        surface.blit(self.dim_screen, self.dim_screen.get_rect(topleft=(0, 0)))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.subtitle, self.subtitle_rect)
        self.draw_buttons(surface)
