import pygame as pg
import math

class simple_forward():
    def __init__(self, owner, speed):
        self.owner = owner
        self.speed = speed
        self.life = 1
    def update(self):
        self.owner.loc_x += self.speed * math.cos(math.radians(self.owner.orient))
        self.owner.loc_y += self.speed * math.sin(math.radians(self.owner.orient))
        self.life = 0

class simple_left_turn():
    def __init__(self, owner, speed):
        self.owner = owner
        self.speed = speed
        self.life = 1
    def update(self):
        self.owner.orient += self.speed
        self.life = 0

class simple_right_turn():
    def __init__(self, owner, speed):
        self.owner = owner
        self.speed = speed
        self.life = 1
    def update(self):
        self.owner.orient -= self.speed
        self.life = 0
