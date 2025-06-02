import pygame as pg

from settings import *


class Exit(pg.sprite.Sprite):
    def __init__(self, game, x: int, y: int, width: int, height: int, color: list[int]):
        super().__init__()
        self.game = game
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass
