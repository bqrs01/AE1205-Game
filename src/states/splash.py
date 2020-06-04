"""
 File: splash.py
 Authors: Mario Padrón Tardáguila & Bryan Quadras
 
 Copyright (c) 2020 Mario Padrón Tardáguila & Bryan Quadras
 
 MIT License
 
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
import pygame as pg

from .. import tools


class SplashScreen(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(SplashScreen, self).__init__()
        # Set next state
        self.next_state = "GAMEPLAY"
        # Set title
        self.title = self.font.render(
            "AE1205 Game (Mario and Bryan)", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

        self.subtitle = self.font.render(
            "Press space to continue", True, pg.Color('darkgreen'))
        self.subtitle_rect = self.subtitle.get_rect(
            center=(self.screen_rect.center[0], self.screen_rect.center[1] + 30))

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True

    def draw(self, surface):
        surface.fill(pg.Color('black'))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.subtitle, self.subtitle_rect)
