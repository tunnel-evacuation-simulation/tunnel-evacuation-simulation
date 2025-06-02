import heapq
import random

import numpy as np
import pygame as pg
from pygame.sprite import Sprite

from settings import *


class Agent(Sprite):
    def __init__(
        self,
        game,
        id: str,
        x: int,
        y: int,
        speed: float,
        panic_factor: float,
        personality: str,
        group_id: str | None,
    ):
        self.groups = game.all_agents
        Sprite.__init__(self, self.groups)
        self.image = pg.image.load(AGENT_IMG)
        self.rect = self.image.get_rect()
        self.game = game
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.panic_factor = panic_factor
        self.personality = personality
        self.group_id = group_id
        self.path = []  

    def update(self):
        if random.random() > self.speed:
            return  # Pomiń ruch w tym ticku

        if random.random() < self.panic_factor:
            dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
            new_x, new_y = self.x + dx, self.y + dy
            if self.can_move_to(new_x, new_y):
                self.move_to(new_x, new_y)
            return

        target = self.get_target()
        if target is None:
            return

        # Oblicz ścieżkę jeśli brak lub cel zmienił się
        if not self.path or self.path[-1] != (
            target.rect.centerx // self.game.tile_size,
            target.rect.centery // self.game.tile_size,
        ):
            self.path = self.calculate_path_to(target)

        if self.path and len(self.path) > 1:
            next_pos = self.path[1]  # Pomijamy [0] bo to aktualna pozycja
            if self.can_move_to(*next_pos):
                self.move_to(*next_pos)
                self.path.pop(0)  # Przesuwamy ścieżkę

        # Sprawdź kolizję z wyjściem
        for exit in self.game.exits:
            exit_cell = (exit.rect.centerx // self.game.tile_size, exit.rect.centery // self.game.tile_size)
            if (self.x, self.y) == exit_cell:
                self.kill()
                break

    def get_target(self):
        if self.group_id is not None:
            leader = self.find_group_leader()
            if leader and leader != self:
                return leader
        return self.find_nearest_exit()

    def find_nearest_exit(self):
        exits = list(self.game.exits)
        current_pos = (self.x * self.game.tile_size, self.y * self.game.tile_size)
        return min(
            exits,
            key=lambda e: abs(current_pos[0] - e.rect.centerx)
            + abs(current_pos[1] - e.rect.centery),
        )

    def find_group_leader(self):
        for agent in self.game.all_agents:
            if agent.group_id == self.group_id and agent.personality == "leader":
                return agent
        return None

    def calculate_path_to(self, target):
        start = (self.x, self.y)
        goal = (target.rect.centerx // self.game.tile_size, target.rect.centery // self.game.tile_size)
        return self.a_star(self.game.grid, start, goal)

    def a_star(self, grid, start, goal):
        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(start, goal), 0, start, [start]))
        visited = set()
        while open_set:
            est_total, cost_so_far, current, path = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                return path
            x, y = current
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                    heapq.heappush(
                        open_set,
                        (
                            cost_so_far + 1 + self.heuristic((nx, ny), goal),
                            cost_so_far + 1,
                            (nx, ny),
                            path + [(nx, ny)],
                        ),
                    )
        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def can_move_to(self, x, y):
        if not (
            0 <= x * self.game.tile_size < SCREEN_WIDTH and 0 <= y * self.game.tile_size < SCREEN_HEIGHT
        ):
            return False
        if (x, y) in self.game.occupied_positions:
            return False
        for wall in self.game.walls:
            if wall.rect.colliderect(
                pg.Rect(x * self.game.tile_size, y * self.game.tile_size, self.game.tile_size, self.game.tile_size)
            ):
                return False
        return True

    def move_to(self, x, y):
        self.game.occupied_positions.discard((self.x, self.y))
        self.x, self.y = x, y
        self.rect.topleft = (x * self.game.tile_size, y * self.game.tile_size)
        self.game.occupied_positions.add((x, y))
