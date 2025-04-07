import random
import sys

import pygame as pg

from agent import Agent
from settings import *
from obstacles import Wall


class Game:

    def __init__(self):
        pg.init()
        random.seed(42)

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.random = random

    def load(self):
        try:
            self.bg_image = pg.image.load(BACKGROUND_IMG)
            print(f"Loading bg image")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.bg_image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill((192, 142, 55))

    def new_instance(self):
        self.all_agents = pg.sprite.Group()
        for _ in range(NUM_OF_AGENTS):
            self.agent = Agent(
                game=self, x=random.randint(0, 40), y=random.randint(10, 25)
            )
        self.walls = pg.sprite.Group()
        wall1 = Wall(self, 0, 75, color=(0, 0, 255))
        wall2 = Wall(self, 0, SCREEN_HEIGHT-85, color=(0, 0, 255))
        self.walls.add(wall1)
        self.walls.add(wall2)
        self.load()

    def run(self):
        self.playing = True

        while self.playing:
            self.time_step = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        if DRAW_GRID:
            self.draw_grid()

        self.all_agents.draw(self.screen)
        self.walls.draw(self.screen)

        pg.display.flip()

    def update(self):
        self.all_agents.update()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
