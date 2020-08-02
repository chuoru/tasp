import pygame
from utils import *
import numpy as np
import math


class DifferentialDriveRobot(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.car_img = pg.transform.scale(game.car_img, (64, 32))
        self.car_img = pg.transform.rotate(self.car_img, 90)
        self.image = self.car_img
        self.rect = self.image.get_rect()
        self.trajectory = [(x, y), (x, y)]
        self.rot = 0
        self.rotate_speed = 1
        self.robot_state = np.array([[x, y, 0, ROBOT_SPEED]]).T
        self.velocity_input = np.array([[16.0, math.pi/8]]).T
        self.rect.centerx = x + 100
        self.rect.centery = y + 100

    def motion_model(self, velocity_input):
        F = np.array([[1.0, 0, 0, 0],
                      [0, 1.0, 0, 0],
                      [0, 0, 1.0, 0],
                      [0, 0, 0, 0]])

        B = np.array([[self.game.dt * math.cos(self.robot_state[2, 0]), 0],
                      [self.game.dt * math.sin(self.robot_state[2, 0]), 0],
                      [0.0, self.game.dt],
                      [1.0, 0.0]])

        self.robot_state = F.dot(self.robot_state) + B.dot(velocity_input)

        return self.robot_state

    def update(self):
        #robot_state = self.motion_model(self.velocity_input)
        #self.rot = robot_state[2, 0]*180/math.pi % 360
        #self.image = pg.transform.rotate(self.car_img, self.rot)
        #self.rect = self.image.get_rect()
        #self.rect.center = (16.0*50, 16.0*50)
        pass

    def draw(self):
        pg.draw.lines(self.game.screen, RED, False, self.trajectory, 3)
