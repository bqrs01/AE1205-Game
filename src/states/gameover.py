import sys
import pygame as pg

from .. import tools


class GameOver(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(GameOver, self).__init__()
        # Set next state
        self.next_state = "SPLASH"

    def startup(self, game_data):
        # Set title
        self.title = self.font.render(
            "Game Over!", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

        self.subtitle = self.font.render(
            f"You got a score of {game_data['final_score']}", True, pg.Color('darkgreen'))
        self.subtitle_rect = self.subtitle.get_rect(
            center=(self.screen_rect.center[0], self.screen_rect.center[1] + 30))

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True

    def draw(self, surface):
        surface.fill(pg.Color('gray'))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.subtitle, self.subtitle_rect)
