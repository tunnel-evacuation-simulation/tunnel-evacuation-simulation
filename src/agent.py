import pygame as pg
from pygame.sprite import Sprite

from settings import *


class Agent(Sprite):
    def __init__(self, game, x: int, y: int) -> None:
        self.groups = game.all_agents

        Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pg.image.load(AGENT_IMG)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    def update(self):
        walls = list(self.game.walls)
        exits = list(self.game.exits)

        # Find min and max y among all walls
        y_coords = [wall.rect.y for wall in walls]

        y_min = min(y_coords)
        y_max = max(y_coords)

        # Then restrict agent movement within this boundary
        new_x = self.x + self.game.random.randint(-1, 1)
        new_y = self.y + self.game.random.randint(-1, 1)

        # Remove agent if it reaches an exit
        for exit in exits:
            if self.rect.colliderect(exit.rect):
                self.kill()
                break

        # Only update if the new position is inside the wall bounds
        if y_min < new_y * TILE_SIZE < y_max-60:
            self.x = new_x
            self.y = new_y

        # Update pixel position for drawing
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)


