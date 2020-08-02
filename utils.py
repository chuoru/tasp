import pygame as pg
import time
WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BGCOLOR = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
ROBOT_SPEED = 6.4
RED = (255, 0, 0)


class Robot(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.p2p_starting_point = tuple([])
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.trajectory = [(x, y), (x, y)]
        self.back_tracking = [(x, y)]
        self.x = round(x, 2)
        self.y = round(y, 2)
        self.start = (self.x, self.y)
        self.rect.centerx = x
        self.rect.centery = y
        self.rot = 0
        self.vx, self.vy = 0, 0
        self.moving_coverage = True
        self.wall_list = []

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if not all(key == 0 for key in keys):
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vx = -ROBOT_SPEED
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vx = ROBOT_SPEED
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vy = - ROBOT_SPEED
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vy = ROBOT_SPEED
            return True
        return False

    def move_straight(self):
        if self.rot == 0:
            self.vx = ROBOT_SPEED
            self.vy = 0
        elif self.rot == 90:
            self.vx = 0
            self.vy = ROBOT_SPEED
        elif self.rot == 180:
            self.vx = -ROBOT_SPEED
            self.vy = 0
        elif self.rot == -90:
            self.vx = 0
            self.vy = -ROBOT_SPEED

    def add_back_tracking(self):
        surroundings = [((int(self.x/TILESIZE) + 1)*TILESIZE + 16, int(self.y/TILESIZE)*TILESIZE + 16),
                        (int(self.x/TILESIZE)*TILESIZE + 16, (int(self.y/TILESIZE) + 1)*TILESIZE + 16),
                        ((int(self.x/TILESIZE) - 1)*TILESIZE + 16, int(self.y/TILESIZE)*TILESIZE + 16),
                        ((int(self.x/TILESIZE))*TILESIZE + 16, (int(self.y/TILESIZE) - 1)*TILESIZE + 16)]

        for wall in self.game.walls:
            self.wall_list.append((wall.x*TILESIZE + 16, wall.y*TILESIZE + 16))
            self.wall_list = list(dict.fromkeys(self.wall_list))

        for surrounding in surroundings:
            if surrounding not in self.wall_list:
                if surrounding not in self.trajectory:
                    self.back_tracking.append(surrounding)
                    self.back_tracking = list(dict.fromkeys(self.back_tracking))

        for back_tracking in self.back_tracking:
            if back_tracking in self.trajectory:
                self.back_tracking.remove(back_tracking)
        if self.p2p_starting_point in self.back_tracking:
            self.back_tracking.remove(self.p2p_starting_point)

    def check_move(self):
        obstacle, free_direction = [], [0, 0, 0, 0]
        surroundings = [
            (int(round(self.x, 2) + TILESIZE), int(round(self.y, 2))),
            (int(round(self.x, 2)), int(round(self.y, 2) - TILESIZE)),
            (int(round(self.x, 2) - TILESIZE), int(round(self.y, 2))),
            (int(round(self.x, 2)), int(round(self.y, 2) + TILESIZE))
        ]

        for (x, y) in self.trajectory:
            obstacle.append((int(x), int(y)))

        obstacle.extend(self.wall_list)
        if surroundings[0] in obstacle:
            free_direction[0] = 1
        if surroundings[1] in obstacle:
            free_direction[1] = 1
        if surroundings[2] in obstacle:
            free_direction[2] = 1
        if surroundings[3] in obstacle:
            free_direction[3] = 1
        if sum(free_direction) == 4:
            return False
        elif sum(free_direction) == 3:
            if free_direction[3] == 0:
                self.rot = 90
            elif free_direction[0] == 0:
                self.rot = 0
            elif free_direction[1] == 0:
                self.rot = -90
            elif free_direction[2] == 0:
                self.rot = 180
            return True
        elif free_direction[1] + free_direction[3] == 2:
            if self.vy != 0:
                if self.__estimate_distance(surroundings[0], self.start) > self.__estimate_distance(surroundings[2], self.start):
                    self.rot = 0
                else:
                    self.rot = 180
            return True
        elif free_direction[0] + free_direction[2] == 2:
            if self.vx != 0:
                if self.__estimate_distance(surroundings[1], self.start) > self.__estimate_distance(surroundings[3], self.start):
                    self.rot = -90
                else:
                    self.rot = 90
            return True
        else:
            return True

    def move_point2point(self):
        compare_list = []
        current = (round(self.x), round(self.y))
        for back_tracking in self.back_tracking:
            compare_list.append(self.__estimate_distance(back_tracking, current))

        destination = self.back_tracking[compare_list.index(min(compare_list))]
        self.x = destination[0]
        self.y = destination[1]
        self.p2p_starting_point = destination
        print("destination, ", destination)

    def collide_with_walls(self):
        for wall in self.wall_list:
            if wall[0] == round(self.x + self.vx * self.game.dt, 2) and wall[1] == round(self.y + self.vy*self.game.dt, 2):
                return False
            return True

    def update_(self):
        if self.get_keys():
            if self.collide_with_walls():
                self.x += self.vx * self.game.dt
                self.x = round(self.x, 2)
                self.y += self.vy * self.game.dt
                self.y = round(self.y, 2)
                self.trajectory.append((self.x, self.y))

        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.add_back_tracking()

    def update(self):
        if self.back_tracking:
            res = self.check_move()
            if res:
                print("Run")
                self.move_straight()

                self.x += self.vx * self.game.dt
                self.x = round(self.x, 2)
                self.y += self.vy * self.game.dt
                self.y = round(self.y, 2)
                self.trajectory.append((self.x, self.y))

            else:
                print("Stop")
                self.move_point2point()
                self.trajectory.append((self.x, self.y))

            self.rect.centerx = self.x
            self.rect.centery = self.y
            # self.rect.centerx = 496
            # self.rect.centery = 48

            self.add_back_tracking()
        else:
            self.x = self.start[0]
            self.y = self.start[1]
            self.trajectory.append((self.x, self.y))
            self.rect.centerx = self.x
            self.rect.centery = self.y
            print("Stopping")

    def draw(self):
        pg.draw.lines(self.game.screen, RED, False, self.trajectory, 3)
        for back_tracking_point in self.back_tracking:
            pg.draw.circle(self.game.screen, RED, back_tracking_point, 5, 1)
        pg.draw.circle(self.game.screen, RED, (int(self.x), int(self.y)), 100, 1)
        # pg.draw.circle(self.game.screen, RED, (496, 48), 100, 1)

    @staticmethod
    def __estimate_distance(position, start):
        return (position[0] - start[0])**2 + (position[1] - start[1])**2


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx = x * TILESIZE + TILESIZE / 2
        self.rect.centery = y * TILESIZE + TILESIZE / 2


