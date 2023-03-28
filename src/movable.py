import pygame as pg
import math
import entity

class Movable(entity.Entity):
    def __init__(self, ref = None):
        super().__init__(ref)
        self.move = 3
        self.turn = 6

    def update(self):
        super().update()

    def move_forward(self):
        rad = math.radians(self.orient)
        self.loc_x -= math.sin(rad)*self.move
        self.loc_y -= math.cos(rad)*self.move

    def move_backward(self):
        rad = math.radians(self.orient)
        self.loc_x += math.sin(rad)*self.move
        self.loc_y += math.cos(rad)*self.move

    def turn_left(self):
        self.orient += self.turn
        if self.orient > 360:
            self.orient -= 360

    def turn_right(self):
        self.orient -= self.turn
        if self.orient < 0:
            self.orient += 360
