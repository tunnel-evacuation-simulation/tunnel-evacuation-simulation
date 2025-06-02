import json
import random
import sys
from os import error

import numpy as np
import pygame as pg

from agent import Agent
from exit import Exit
from obstacles import Wall
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMG, FPS, DRAW_GRID, GRID_COLOR
import csv
import datetime



class Game:
    def __init__(self, simulation_file: str, output_path: str):
        self.occupied_positions = set()
        self.all_agents = pg.sprite.Group()
        self.title = str()
        self.tile_size = str()
        self.initSettings(simulation_file)

        pg.init()
        random.seed(42)

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(self.title)

        self.simulation_file_path = simulation_file
        self.output_file_path = output_path

        self.clock = pg.time.Clock()
        self.random = random



    def initSettings(self, simulation_file: str):
        with open(simulation_file, "r") as sim:
            f = json.load(sim)

            self.tile_size = f["tile_size"]
            self.title = f["title"]

    def init_output(self, output_file: str):
        """
        Inits the output file with the first row which includes: timestamp, agent_id, x, y
        """
        timestamp = datetime.datetime.now().isoformat()
        print(datetime.datetime.now().isoformat())

        try:
            with open(output_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                header = ['timestamp']
                for i in range(len(self.all_agents)):
                    header.append(f'agent{i+1}')
                writer.writerow(header)


        except FileNotFoundError as err:
            return f"Could not find {self.output_file_path} file.\nMake sure the file exists in the correct location: {err}"

    def load(self):
        try:
            self.bg_image = pg.image.load(BACKGROUND_IMG)
            print("Loading bg image")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.bg_image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill((51, 52, 70))

    def init_agents(self):
        self.all_agents = pg.sprite.Group()
        self.occupied_positions = set()

        try:
            with open(self.simulation_file_path, "r") as sim:
                f = json.load(sim)

                self.grid = [
                    [0 for _ in range(SCREEN_HEIGHT // self.tile_size)]
                    for _ in range(SCREEN_WIDTH // self.tile_size)
                ]

                for agent_data in f["agents"]:
                    id = agent_data["id"]
                    position = agent_data["initial_position"]
                    speed = agent_data["speed"]
                    panic_factor = agent_data["panic_factor"]
                    personality = agent_data["personality"]
                    group_id = agent_data["group_id"]

                    if (position[0], position[1]) not in self.occupied_positions:
                        new_agent = Agent(
                            game=self,
                            id=id,
                            x=position[0],
                            y=position[1],
                            speed=speed,
                            panic_factor=panic_factor,
                            personality=personality,
                            group_id=group_id,
                        )

                        new_agent.rect.topleft = (
                            position[0] * self.tile_size,
                            position[1] * self.tile_size,
                        )

                        self.all_agents.add(new_agent)
        except FileNotFoundError as err:
            return f"Could not find {self.simulation_file_path} file.\nMake sure the file exists in the correct location: {err}"

    def init_obstacles(self):
        try:
            with open(self.simulation_file_path, "r") as sim:
                f = json.load(sim)

                self.walls = pg.sprite.Group()
                for wall in f["walls"]:
                    wall_x, wall_y = wall["initial_position"]
                    wall_width = wall["width"]
                    wall_height = wall["height"]
                    wall_color = wall["color"]

                    new_wall = Wall(
                        self,
                        wall_x * self.tile_size,
                        wall_y * self.tile_size,
                        wall_width * self.tile_size,
                        wall_height * self.tile_size,
                        wall_color,
                    )
                    self.walls.add(new_wall)
        except FileNotFoundError as err:
            return f"Could not find {self.simulation_file_path} file.\nMake sure the file exists in the correct location: {err}"

    def init_exits(self):
        try:
            with open(self.simulation_file_path, "r") as sim:
                f = json.load(sim)
                self.exits = pg.sprite.Group()
                for exit in f["exits"]:
                    exit_x, exit_y = exit["initial_position"]
                    exit_width = exit["width"]
                    exit_height = exit["height"]
                    exit_color = exit["color"]

                    new_exit = Exit(
                        self,
                        exit_x * self.tile_size,
                        exit_y * self.tile_size,
                        exit_width * self.tile_size,
                        exit_height * self.tile_size,
                        exit_color,
                    )
                    self.exits.add(new_exit)

        except FileNotFoundError as err:
            return f"Could not find {self.simulation_file_path} file.\nMake sure the file exists in the correct location: {err}"

    def run(self):
        self.playing = True
        self.init_output(self.output_file_path)

        while self.playing:
            self.time_step = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.write_output(self.output_file_path)

    def write_output(self, output_file):
        """
        Writes the current timestamp and position of each agent to a CSV file.
        Each row includes: timestamp, agent_id, x, y
        """
        timestamp = datetime.datetime.now().strftime("%X")
        print(datetime.datetime.now().isoformat())

        try:
            with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)

                row = [timestamp]
                for agent in self.all_agents:
                    row.append(f'({agent.x}; {agent.y})')  # values as strings in brackets
                writer.writerow(row)



        except FileNotFoundError as err:
            return f"Could not find {self.output_file_path} file.\nMake sure the file exists in the correct location: {err}"

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

        for agent in self.all_agents:
            if agent.path:
                for pos in agent.path:
                    rect = pg.Rect(
                        pos[0] * self.tile_size + self.tile_size // 4,
                        pos[1] * self.tile_size + self.tile_size // 4,
                        self.tile_size // 2,
                        self.tile_size // 2,
                    )
                    pg.draw.rect(self.screen, (0, 0, 255), rect)
        pg.display.flip()

    def update(self):
        self.all_agents.update()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, self.tile_size):
            pg.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, self.tile_size):
            pg.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
