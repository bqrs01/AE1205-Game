"""
 File: l.py
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

import pygame as pg
import sys
# This code is licensed as CC0 1.0 (https: // creativecommons.org/publicdomain/zero/1.0/legalcode).


class Game(object):
    """
    A single instance of this class is responsible for 
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event 
    queue, framerate, updating the display, etc.). 
    and its run method serves as the "game loop".
    """

    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.

        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state 
        """
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update active state.

        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)

    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


class GameState(object):
    """
    Parent class for individual game states to inherit from. 
    """

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        persistent: a dict passed from state to state
        """
        self.persist = persistent

    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass

    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame. 

        dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass


class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.font.render(
            "Splash Screen", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            self.persist["screen_color"] = "gold"
            self.done = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.persist["screen_color"] = "dodgerblue"
            self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pg.Color(color)
        if color == "dodgerblue":
            text = "You clicked the mouse to get here"
        elif color == "gold":
            text = "You pressed a key to get here"
        self.title = self.font.render(text, True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.title_rect.center = event.pos

    def update(self, dt):
        self.rect.move_ip(self.x_velocity, 0)
        if (self.rect.right > self.screen_rect.right
                or self.rect.left < self.screen_rect.left):
            self.x_velocity *= -1
            self.rect.clamp_ip(self.screen_rect)

    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.title, self.title_rect)
        pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    states = {"SPLASH": SplashScreen(),
              "GAMEPLAY": Gameplay()}
    game = Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()
