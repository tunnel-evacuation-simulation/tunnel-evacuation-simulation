import random

import numpy as np
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
        old_x = self.x
        old_y = self.y
        walls = list(self.game.walls)
        exits = list(self.game.exits)
        agents = list(self.game.all_agents)

        # Find min and max y among all walls
        y_coords = [wall.rect.y for wall in walls]
        y_min = min(y_coords)
        y_max = max(y_coords)

        # Get current pixel position
        current_pos = (self.x * TILE_SIZE, self.y * TILE_SIZE)

        # Find nearest exit based on Euclidean distance
        nearest_exit = None
        min_dist_sq = float('inf')
        for exit in exits:
            exit_pos = exit.rect.center
            dx = current_pos[0] - exit_pos[0]
            dy = current_pos[1] - exit_pos[1]
            dist_sq = dx * dx + dy * dy
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                nearest_exit = exit

        # Compute direction to move toward nearest exit
        target_x = nearest_exit.rect.centerx // TILE_SIZE
        target_y = nearest_exit.rect.centery // TILE_SIZE

        dx = 0
        dy = 0

        if random.randint(1,10) < 9:
            if target_x > self.x:
                dx = 1
            elif target_x < self.x:
                dx = -1
            else:
                dx = 0

            if target_y > self.y:
                dy = 1
            elif target_y < self.y:
                dy = -1
            else:
                dy = 0
        else:
            dx = random.randint(-1,1)
            dy = random.randint(-1,1)

        # Try to move (one step toward exit)
        new_x = self.x + dx
        new_y = self.y + dy

        # Remove agent if it reaches an exit
        for exit in exits:
            if self.rect.colliderect(exit.rect):
                self.kill()
                break

        # Add check for already occupied cells
        # TODO check rectangle instead of position f.e. self.rect.colliderect(agent.rect)
        if (new_x, new_y) not in self.game.occupied_positions:
            self.game.occupied_positions.discard((self.x, self.y))

            # Only update if the new position is inside the wall bounds
            if y_min < new_y * TILE_SIZE < y_max - GRID_HEIGHT:
                self.y = new_y

            if 0 < new_x * TILE_SIZE < SCREEN_WIDTH - GRID_WIDTH:
                self.x = new_x

            self.game.occupied_positions.add((new_x, new_y))

            # Update pixel position for drawing
            self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)






