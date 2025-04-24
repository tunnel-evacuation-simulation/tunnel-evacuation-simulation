import pygame as pg

from settings import *


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, width=WALL_WIDTH, height=WALL_HEIGHT, color=WALL_COLOR):
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
