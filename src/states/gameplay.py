import sys
import pygame as pg
import os

from .. import tools
from ..components import player, enemy, bullet

vec = pg.math.Vector2


class GamePlay(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(GamePlay, self).__init__()
        self.heartImages = {}
        self.heartImage = self.load_image(50)
        self.score_message = self.font.render(
            "Score: 0", True, pg.Color('black'))
        self.score_message_rect = self.score_message.get_rect(center=(50, 20))
        self.break_message = self.font.render(
            "Cooldown", True, pg.Color('green'))
        self.break_message_rect = self.score_message.get_rect(center=(50, 60))
        self.onBreak = False
        self.timer = 0

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "GAMEOVER"
                self.done = True
            self.player.add_direction(event.key)
        elif event.type == pg.KEYUP:
            self.player.pop_direction(event.key)
        elif event.type == pg.MOUSEMOTION:
            self.player.update_angle(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.player.shoot()

    def startup(self, game_data):
        self.game_data = game_data
        self.statsManager = StatsManager()
        self.bulletManager = bullet.BulletManager()
        self.enemyManager = enemy.EnemyManager(self.bulletManager)
        self.player = player.Player(self.bulletManager, self.statsManager)

        self.enemyManager.generate(1)

    def update(self, dt):
        if not self.statsManager.gameOver:
            self.timer -= dt
            if round(self.timer) <= 0:
                if self.onBreak:
                    self.onBreak = False
                self.timer = 0
                if not (self.player.safe_zone):
                    self.enemyManager.generate(2)
            self.player.update(dt)
            self.enemyManager.update(
                self.player.exact_pos[0], self.player.exact_pos[1], self.player.isMoving, self.player.safe_zone, dt)
            self.bulletManager.update(self.player, self.enemyManager)

            self.score_message = self.font.render(
                f"Score: {self.statsManager.score}", True, pg.Color('black'))

            # If there are no enemies left...
            if (len(self.enemyManager) == 0) and self.timer != 0:
                self.timer = 3500
                self.onBreak = True
                # self.enemyManager.generate(3)
        else:
            # Game over. Switch to next state.
            self.next_state = "GAMEOVER"
            self.game_data['final_score'] = self.statsManager.score
            self.done = True

            # if len(pg.sprite.spritecollide(self.player, self.enemyManager, False)) > 0:
            # print("Game over")
            #self.quit = True
            # print(self.x_velocity, self.y_velocity)d
            # self.rect.move_ip(self.x_velocity, (-1) * self.y_velocity)
            # if (self.rect.rightw > self.screen_rect.right or self.rect.left < self.screen_rect.left):
            #     self.x_velocity *= -1
            #     self.rect.clamp_ip(self.screen_rect)
            # if (self.rect.top < self.screen_rect.top or self.rect.bottom > self.screen_rect.bottom):
            #     self.y_velocity *= -1
            #     self.rect.clamp_ip(self.screen_rect)

    def draw(self, surface):
        surface.fill(pg.Color('white'))
        #pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)
        self.player.draw(surface)
        self.enemyManager.draw(surface)
        self.bulletManager.draw(surface)
        # pg.draw.lines(surface, (0, 0, 0), False, [
        #     self.player.rect.center, self.player.mouse_position])
        surface.blit(self.score_message, self.score_message_rect)
        self.draw_health(self.statsManager.health, surface)
        if self.onBreak:
            surface.blit(self.break_message, self.break_message_rect)

    def load_image(self, health):
        if health in self.heartImages.keys():
            return self.heartImages[health]
        else:
            image = pg.image.load(
                os.path.join(os.getcwd(), f"src/images/hearts_{health}.png"))
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

        if self.health <= 5:
            self.health = 0
            self.gameOver = True

        print(f"Health: {self.health}")
