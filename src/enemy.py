import pygame as pg
import movable

class Enemy(movable.Movable):
    def __init__(self, ref):
        super().__init__(ref)
        self.max_hp = 100
        self.health_point = 100
        self.loc_x = 10
        self.loc_y = 10
        #self.ori_image = pg.Surface((64, 64))
        #self.ori_image.fill((255,255,255))
        #self.ori_image.set_colorkey((255,255,255))
        #self.image = self.ori_image