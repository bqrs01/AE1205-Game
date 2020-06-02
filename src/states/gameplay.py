import sys
import pygame as pg

from .. import tools
from ..components import player, enemy, bullet


class GamePlay(tools.State):
    def __init__(self):
        # Call super to initialise everything needed
        super(GamePlay, self).__init__()
        # self.rect = pg.Rect((0, 0), (64, 64))
        # self.x_velocity = 1
        # self.y_velocity = -1
        self.bulletManager = bullet.BulletManager()
        self.enemyManager = enemy.EnemyManager(self.bulletManager)
        self.player = player.Player(self.bulletManager)
        self.enemyManager.generate(1)
        self.exit_message = self.font.render(
            "Press ESC to quit.", True, pg.Color('black'))
        self.exit_message_rect = self.exit_message.get_rect(center=(85, 20))
        self.timer = 0

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            self.player.add_direction(event.key)
            # if event.key == pg.K_UP:
            #     self.y_velocity = 1
            # if event.key == pg.K_DOWN:
            #     self.y_velocity = -1
            # if event.key == pg.K_RIGHT:
            #     self.x_velocity = 1
            # if event.key == pg.K_LEFT:
            #     self.x_velocity = -1
        elif event.type == pg.KEYUP:
            self.player.pop_direction(event.key)
        elif event.type == pg.MOUSEMOTION:
            self.player.update_angle(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.player.shoot()

    def update(self, dt):
        self.timer += dt
        if round(self.timer) >= 10000:
            self.timer = 0
            self.enemyManager.generate(5)
        self.player.update()
        self.enemyManager.update(
            self.player.exact_pos[0], self.player.exact_pos[1], self.player.isMoving)
        self.bulletManager.update(self.player, self.enemyManager)

        if len(pg.sprite.spritecollide(self.player, self.enemyManager, False)) > 0:
            print("Game over")
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
        surface.blit(self.exit_message, self.exit_message_rect)
