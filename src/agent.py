import pygame as pg
from pygame.sprite import Sprite

from settings import *


class Agent(Sprite):
    def __init__(self, game, x: int, y: int) -> None:
        self.groups = game.all_agents

        Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(AGENT_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.x = self.x + self.game.random.randint(-1, 1)
        self.y = self.y + self.game.random.randint(-1, 1)
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
