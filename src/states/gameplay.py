"""
 File: gameplay.py
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
import pygame as pg
import os

from .. import tools, prepare
from ..components import player, enemy, bullet, explosion

vec = pg.math.Vector2


class GamePlay(tools.State):
    def __init__(self):
        # Call super to initialise everything needed.
        super(GamePlay, self).__init__()
        # Load background image.
        self.backgroundImage = pg.image.load(
            os.path.join(os.getcwd(), "src/images/background.png")).convert()
        self.backgroundImage_rect = self.backgroundImage.get_rect(
            topleft=(0, 0))
        # Initialise dictionary for health bar.
        self.heartImages = {}
        self.heartImage = self.load_image(50)
        # Initialise score message text surface.
        self.score_message = self.font.render(
            "Score: 0", True, pg.Color('black'))
        self.score_message_rect = self.score_message.get_rect(center=(50, 20))
        # Initialise break message text surface and initialise onBreak, timer properties.
        self.break_message = self.font.render(
            "Cooldown", True, pg.Color('green'))
        self.break_message_rect = self.score_message.get_rect(center=(50, 60))
        self.onBreak = False
        self.timer = 0
        # Initialise property isPaused to False.
        self.isPaused = False
        self.paused_font = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 50)
        self.paused_font_sub = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 35)
        self.paused_message = self.paused_font.render(
            "Paused", True, pg.Color('green'))
        self.paused_message_rect = self.paused_message.get_rect(
            center=prepare.SCREEN_CENTER)
        self.paused_message_subtitle = self.paused_font_sub.render(
            "Press p to start playing", True, pg.Color('red'))
        self.paused_message_subtitle_rect = self.paused_message_subtitle.get_rect(
            center=(prepare.SCREEN_CENTER[0], prepare.SCREEN_CENTER[1]+50))
        self.dim_screen = pg.Surface(prepare.SCREEN_SIZE).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.isStart = False
        self.start_message = self.paused_font_sub.render(
            "Game is about to start!", True, pg.Color('green'))
        self.start_message_rect = self.start_message.get_rect(
            center=prepare.SCREEN_CENTER)
        self.last_update = None

    def handle_event(self, event):
        """Function to handle pygame events."""
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "GAMEOVER"
                self.game_data['final_score'] = self.statsManager.score
                self.done = True
            elif event.key == pg.K_p:
                self.isPaused = not self.isPaused
            else:
                self.player.add_direction(event.key)
        elif event.type == pg.KEYUP:
            self.player.pop_direction(event.key)
        elif event.type == pg.MOUSEMOTION:
            self.player.update_angle(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.player.shoot()

    def startup(self, game_data):
        """Startup function that sets up all game constructs."""
        self.game_data = game_data
        self.statsManager = StatsManager()
        self.bulletManager = bullet.BulletManager()
        self.enemyManager = enemy.EnemyManager(self.bulletManager)
        self.explosionManager = explosion.ExplosionManager()
        self.player = player.Player(
            self.bulletManager, self.statsManager, self.explosionManager)
        # Generate one enemy at start of game.
        self.enemyManager.generate(1)
        self.isStart = True
        self.last_update = pg.time.get_ticks()

    def update(self, dt):
        """Update function to update sprite position and graphics."""
        if not self.statsManager.gameOver:
            if self.isPaused:
                # Do not update game if paused or about to start.
                pass
            elif self.isStart:
                now = pg.time.get_ticks()
                if (now - self.last_update) > 3000:
                    self.isStart = False
            else:
                self.timer -= dt
                if round(self.timer) <= 0:
                    if self.onBreak:
                        self.onBreak = False
                    self.timer = 3000
                    if not (self.player.safe_zone):
                        self.enemyManager.generate(2)
                self.player.update(dt)
                self.enemyManager.update(self.player,
                                         self.player.exact_pos[0], self.player.exact_pos[1], self.player.isMoving, self.player.safe_zone, dt)
                self.bulletManager.update(
                    self.player, self.enemyManager, self.explosionManager)
                self.explosionManager.update()

                self.score_message = self.font.render(
                    f"Score: {self.statsManager.score}", True, pg.Color('black'))

                # If there are no enemies left...
                if (len(self.enemyManager) == 0) and not self.onBreak and not self.player.safe_zone:
                    self.enemyManager.generate(2)
        else:
            # Game over. Switch to next state.
            self.next_state = "GAMEOVER"
            self.game_data['final_score'] = self.statsManager.score
            self.done = True

    def draw(self, surface):
        """Draw function to draw all game elements on screen."""
        surface.blit(self.backgroundImage, self.backgroundImage_rect)
        # surface.fill(pg.Color('white'))
        #pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)
        self.player.draw(surface)
        self.enemyManager.draw(surface)
        self.bulletManager.draw(surface)
        self.explosionManager.draw(surface)
        # pg.draw.lines(surface, (0, 0, 0), False, [
        #     self.player.rect.center, self.player.mouse_position])
        surface.blit(self.score_message, self.score_message_rect)
        self.draw_health(self.statsManager.health, surface)
        if self.onBreak:
            surface.blit(self.break_message, self.break_message_rect)
        if self.isPaused:
            surface.blit(self.dim_screen, (0, 0))
            surface.blit(self.paused_message, self.paused_message_rect)
            surface.blit(self.paused_message_subtitle,
                         self.paused_message_subtitle_rect)
        if self.isStart:
            surface.blit(self.dim_screen, (0, 0))
            surface.blit(self.start_message, self.start_message_rect)

    def load_image(self, health):
        if health in self.heartImages.keys():
            return self.heartImages[health]
        else:
            image = pg.image.load(
                os.path.join(os.getcwd(), f"src/images/hearts_{health}.png")).convert()
            self.heartImages[health] = image
            return image

    def draw_health(self, health, screen):
        self.heartImage = self.load_image(health)
        screen.blit(self.heartImage, self.heartImage.get_rect(center=(50, 35)))


class StatsManager():
    def __init__(self):
        self.score = 0.0
        self.health = 50
        self.gameOver = False

    def addScore(self, points):
        self.score += points
        print(f"Score: {self.score}")

    def dropHealth(self, dropBy=10):
        self.health -= dropBy

        if self.health < 5:
            self.health = 0
            self.gameOver = True

        print(f"Health: {self.health}")
