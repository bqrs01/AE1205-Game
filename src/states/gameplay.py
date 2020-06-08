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
import threading

from .. import tools, prepare
from ..components import player, enemy, bullet, explosion, powerup

# Shortcut for vector
vec = pg.math.Vector2


class GamePlay(tools.State):
    def __init__(self):
        # Call super to initialise everything needed.
        super(GamePlay, self).__init__()

        # BACKGROUND
        self.backgroundImage = pg.image.load(
            os.path.join(os.getcwd(), "src/images/background.png")).convert()
        self.backgroundImage_rect = self.backgroundImage.get_rect(
            topleft=(0, 0))

        # HEALTH DISPLAY
        self.heartImages = {}
        self.heartImage = self.load_image(50)
        self.sub_font = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 25)

        # INFOBAR
        self.infobar = pg.Surface((160, 95))
        self.infobar_rect = self.infobar.get_rect(topleft=(10, 10))

        # SCORE MESSAGE
        self.score_message = self.sub_font.render(
            "Score: 0.0", True, pg.Color('black'))
        self.score_message_rect = self.score_message.get_rect(topleft=(5, 10))

        # Initialise break message text surface and initialise onBreak, timer properties.
        self.break_message = self.sub_font.render(
            "Cooldown", True, pg.Color('red'))
        self.break_message_rect = self.score_message.get_rect(topleft=(5, 60))
        self.onBreak = False
        self.timer = 0

        # Initialise property isPaused to False.
        self.isPaused = False
        self.isEnd = False

        # PAUSED SCREEN
        self.paused_font = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 60)
        self.paused_font_sub = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 35)
        self.paused_message = self.paused_font.render(
            "Paused", True, pg.Color('green'))
        self.paused_message_rect = self.paused_message.get_rect(
            center=(prepare.SCREEN_CENTER[0], prepare.SCREEN_CENTER[1]-40))
        # self.paused_message_subtitle = self.paused_font_sub.render(
        #     "Press ESC to start playing", True, pg.Color('red'))
        # self.paused_message_subtitle_rect = self.paused_message_subtitle.get_rect(
        #     center=(prepare.SCREEN_CENTER[0], prepare.SCREEN_CENTER[1]+50))
        self.dim_screen = pg.Surface(prepare.SCREEN_SIZE).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.button_names = ["resumebutton", "menubutton"]
        self.button_pos = [380, 450]
        self.button_size = [(180, 54), (180, 54)]
        self.button_states = ["NONE", "MAINSCREEN"]
        self.buttons = []
        self.buttons_focused = []
        self.buttons_rects = []
        self.focused_button = -1

        self.mousepos = (0, 0)

        self.get_button_images()

        # START SCREEN
        self.isStart = False
        self.start_message = self.paused_font_sub.render(
            "Game is about to start!", True, pg.Color('green'))
        self.start_message_rect = self.start_message.get_rect(
            center=prepare.SCREEN_CENTER)
        self.last_update = None

        # MISCALLANEOUS
        self.surface = pg.Surface(prepare.SCREEN_SIZE)
        self.bgmusic = {}
        self.sub_font_2 = pg.font.Font(os.path.join(
            os.getcwd(), "src/fonts/FORTE.TTF"), 15)

    def render_infobar(self, surface):
        """Function to render and blit the infobar."""
        self.infobar.fill((0, 255, 255))
        self.infobar.set_alpha(80)
        self.infobar.blit(self.score_message, self.score_message_rect)
        if self.onBreak:
            self.infobar.blit(self.break_message, self.break_message_rect)
        self.draw_health(self.statsManager.health, self.infobar)
        surface.blit(self.infobar, self.infobar_rect)

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
            self.isPaused = False
            if not self.button_states[self.focused_button] == "NONE":
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

    def handle_event(self, event):
        """Function to handle pygame events."""
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if not self.isStart:
                    self.isPaused = not self.isPaused
            else:
                self.player.add_direction(event.key)
        elif event.type == pg.KEYUP:
            self.player.pop_direction(event.key)
        elif event.type == pg.MOUSEMOTION:
            self.player.update_angle(event.pos)
            self.mousepos = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            if self.isPaused:
                self.button_selected()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if not self.isPaused and not self.isStart and not self.statsManager.infinity:
                self.player.shoot()

    def startup(self, game_data):
        """Startup function that sets up all game constructs."""
        self.game_data = game_data
        self.statsManager = StatsManager()
        self.soundManager = tools.SoundManager('prefs.json')
        self.powerupManager = powerup.PowerupManager(self.statsManager)
        self.bulletManager = bullet.BulletManager(
            self.soundManager, self.powerupManager)
        self.enemyManager = enemy.EnemyManager(self.bulletManager)
        self.explosionManager = explosion.ExplosionManager()
        self.enemyAI = enemy.EnemyAI(self.statsManager)
        self.player = player.Player(
            self.bulletManager, self.statsManager, self.explosionManager)
        self.isStart = True
        self.current_song = self.sub_font_2.render(
            f"Song: {self.bgmusic['song_name']}", True, pg.color.Color('yellow'))
        self.current_song_rect = self.current_song.get_rect(
            bottomleft=(15, 690))
        self.last_update = pg.time.get_ticks()

        self.isEnd = False
        self.isPaused = False

    def update(self, dt):
        """Update function to update sprite position and graphics."""
        if not self.statsManager.gameOver:
            if self.isPaused:
                # Do not update game if paused
                self.check_if_focused()
            elif self.isStart:
                now = pg.time.get_ticks()
                if (now - self.last_update) > 3000:
                    self.isStart = False
                    self.enemyManager.generate(1)
            else:
                self.timer -= dt
                if round(self.timer) <= 0:
                    if self.onBreak:
                        self.onBreak = False
                    self.timer = 3500
                    self.enemyManager.generate(self.enemyAI.no_to_generate())
                self.player.update(dt)
                self.enemyManager.update(self.player,
                                         self.player.exact_pos[0], self.player.exact_pos[1], self.player.isMoving, self.player.safe_zone, dt)
                self.bulletManager.update(
                    self.player, self.enemyManager, self.explosionManager)
                self.explosionManager.update()
                self.powerupManager.update(self.player, self.statsManager)

                self.score_message = self.sub_font.render(
                    f"Score: {self.statsManager.score}", True, pg.Color('black'))

                self.current_song = self.sub_font_2.render(
                    f"Song: {self.bgmusic['song_name']}", True, pg.color.Color('yellow'))

                # If there are no enemies left...
                if (len(self.enemyManager) == 0):
                    if not self.onBreak and not self.player.safe_zone:
                        self.onBreak = True
                        self.timer = 1500
                    if self.player.safe_zone:
                        self.onBreak = False
        else:
            # Game over. Switch to next state.
            self.isEnd = True
            self.next_state = "GAMEOVER"
            self.game_data['final_score'] = self.statsManager.score
            self.game_data['game_screen'] = self.surface
            self.bgmusic["pause_music"](3.5)
            self.done = True

    def draw(self, surface):
        """Draw function to draw all game elements on screen."""
        surface.blit(self.backgroundImage, self.backgroundImage_rect)
        self.player.draw(surface)
        self.enemyManager.draw(surface)
        self.bulletManager.draw(surface)
        self.explosionManager.draw(surface)
        self.powerupManager.draw(surface)

        self.render_infobar(surface)

        if not self.isEnd:
            surface.blit(self.current_song, self.current_song_rect)

        if self.isPaused:
            surface.blit(self.dim_screen, (0, 0))
            surface.blit(self.paused_message, self.paused_message_rect)
            # surface.blit(self.paused_message_subtitle,
            #              self.paused_message_subtitle_rect)
            self.draw_buttons(surface)
        if self.isStart:
            surface.blit(self.dim_screen, (0, 0))
            surface.blit(self.start_message, self.start_message_rect)

        self.surface = surface.copy()

    def load_image(self, health):
        """Function to load and save images of the different health states."""
        if health in self.heartImages.keys():
            return self.heartImages[health]
        else:
            image = pg.image.load(
                os.path.join(os.getcwd(), f"src/images/hearts_{health}.png")).convert_alpha()
            image.set_colorkey((0, 0, 0))
            image = pg.transform.scale(image, (102, 18))
            self.heartImages[health] = image
            return image

    def draw_health(self, health, screen):
        """Draw heart state to screen."""
        self.heartImage = self.load_image(health)
        screen.blit(self.heartImage, self.heartImage.get_rect(topleft=(5, 42)))


class StatsManager():
    def __init__(self):
        self.score = 0.0
        self.health = 50
        self.kills = 0
        self.gameOver = False
        self.multiplier = 1.0
        self.infinity = False
        self.powerup_active = False

    def set_multiplier(self, mult, resetAfter=20):
        """Set multiplier to a value temporarily. Useful for powerup."""
        self.multiplier = mult
        self.powerup_active = True
        threading.Timer(resetAfter, self.reset_multiplier).start()

    def reset_multiplier(self):
        self.multiplier = 1.0
        self.powerup_active = False

    def set_infinity(self, resetAfter=15):
        """Set infinity on temporarily. Useful for powerup."""
        self.infinity = True
        self.powerup_active = True
        threading.Timer(resetAfter, self.reset_infinity).start()

    def reset_infinity(self):
        self.infinity = False
        self.powerup_active = False

    def reset_powerups(self):
        """Reset powerups."""
        self.infinity = False
        self.multiplier = 1.0
        self.powerup_active = False

    def addKill(self):
        """Add kills to tally."""
        self.kills += 1

    def addScore(self, points):
        """Add score to tally."""
        self.score += points * self.multiplier
        # print(f"Score: {self.score}")

    def dropHealth(self, dropBy=10):
        """Reduce player's health."""
        self.health -= dropBy
        if self.health < 5:
            self.health = 0
            threading.Timer(0.5, self.declareGameOver).start()

    def declareGameOver(self):
        """Declare game over."""
        self.gameOver = True
