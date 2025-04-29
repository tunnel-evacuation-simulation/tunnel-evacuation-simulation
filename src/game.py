import random
import sys

import pygame as pg

from agent import Agent
from settings import *
from obstacles import Wall
from exit import Exit


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
        # TODO setting new instances
        self.all_agents = pg.sprite.Group()
        for _ in range(NUM_OF_AGENTS):
            is_on_another_agent = True
            while is_on_another_agent:
                is_on_another_agent = False

                x = random.randint(0, int(SCREEN_WIDTH / TILE_SIZE) - 10)
                y = random.randint(0, int(SCREEN_HEIGHT / TILE_SIZE) - 10)

                new_agent = Agent(game=self, x=x, y=y)
                new_agent.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

                for agent in self.all_agents:
                    if new_agent.rect.colliderect(agent.rect):
                        new_agent.kill()
            self.all_agents.add(new_agent)

        self.walls = pg.sprite.Group()
        wall1 = Wall(self, WALL_1_X, WALL_1_Y, color=WALL_COLOR)
        wall2 = Wall(self, WALL_2_X, WALL_2_Y, color=WALL_COLOR)
        self.walls.add(wall1)
        self.walls.add(wall2)

        self.exits = pg.sprite.Group()
        self.exits.add(Exit(game=self, x=EXIT_1_X, y=EXIT_1_Y))
        self.exits.add(Exit(game=self, x=EXIT_2_X, y=EXIT_2_Y))
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
        self.exits.draw(self.screen)

        pg.display.flip()

    def update(self):
        self.all_agents.update()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
