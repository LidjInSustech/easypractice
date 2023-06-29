import pygame as pg
import math

class base_move():
    def __init__(self):
        self.life = 1

class simple_forward(base_move):
    def __init__(self, owner, speed):
        self.owner = owner
        self.speed = speed
    def update(self):
        #print(f"x: {self.owner.loc_x}, y: {self.owner.loc_y}, orient: {self.owner.orient}")
        self.owner.loc_x += self.speed * math.cos(math.radians(self.owner.orient))
        self.owner.loc_y += self.speed * math.sin(math.radians(self.owner.orient))
        self.life = 0

class simple_turn(base_move):
    def __init__(self, owner, speed):
        self.owner = owner
        self.speed = speed
    def update(self):
        self.owner.orient += self.speed
        self.life = 0

