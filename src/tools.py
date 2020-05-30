import sys
import pygame as pg


class Game(object):
    def __init__(self, screen, states, start_state):
        """
        Initialise the Game object, and save some important variables.
        """
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        """Events are passed to current state"""
        for event in pg.event.get():
            self.state.handle_event(event)

    def switch_state(self):
        """Switch to the next state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        game_data = self.state.game_data  # Persistent data
        self.state = self.states[self.state_name]
        self.state.startup(game_data)

    def update(self, dt):
        """Check for state switch and update state if needed"""
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.switch_state()
        self.state.update(dt)

    def draw(self):
        """Pass surface to state for drawing"""
        self.state.draw(self.screen)

    def run(self):
        """Game loop will run in the while loop here"""
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


class State(object):
    """Base class for game states"""

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.game_data = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, game_data):
        """Called when state is about to become active or resumes being active."""
        self.game_data = game_data

    def handle_event(self, event):
        """Handle events passed by Game"""
        pass

    def update(self, dt):
        """Update the state."""
        pass

    def draw(self, surface):
        """Draw scene to screen"""
        pass


class _BaseSprite(pg.sprite.Sprite):
    """The base class for all types of sprites"""

    def __init__(self, pos, size, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rect = pg.Rect(pos, size)
        self.exact_pos = list(self.rect.topleft)
        self.old_pos = self.exact_pos[:]

    def reset_position(self, value):
        """
        Set sprite location to new point. By default `value`
        specifies a position in the topleft corner.
        """
        setattr(self.rect, "topleft", value)
        self.exact_pos = list(self.rect.topleft)
        self.old_pos = self.exact_pos[:]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
