
import pygame as pg
import sys
from utils import *
from os import path
from robot import *

WIDTH = 1024
HEIGHT = 768
TITLE = "Coverage Path Planning"
FPS = 60
BGCOLOR = (40, 40, 40)
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
LIGHTGREY = (100, 100, 100)
YELLOW = (0, 255, 255)


class Environment:
    def __init__(self):
        self.map_data = []
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.playing = True

    def load_data(self):
        sim_folder = path.dirname(__file__)
        self.car_img = pg.image.load(path.join(sim_folder, "robot.png")).convert_alpha()
        with open(path.join(sim_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.trajectories = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
        self.robot = Robot(self, TILESIZE * 3/2, TILESIZE * 3/2)

    def run(self):
        # game loop - set self.playing = False to end the game
        while self.playing:
            # self.dt = self.clock.tick(FPS)/1000
            self.dt = 1
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.robot.draw()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                x = int(event.pos[0]/TILESIZE)
                y = int(event.pos[1]/TILESIZE)
                Wall(self, x, y)

            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Environment()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()


