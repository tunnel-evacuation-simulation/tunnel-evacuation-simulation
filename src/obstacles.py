import pygame as pg

from settings import *


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, width=SCREEN_WIDTH, height=10, color=(100, 100, 100)):
        super().__init__()
        self.game = game
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # For static walls, this might not do anything
        pass
