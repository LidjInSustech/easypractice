import pygame as pg
import visibles

class Fliping(visibles.Movable):
    def __init__(self, owner, loc = pg.math.Vector2(), orientation = 0, images = None, radius = None, properties = None):
        super().__init__(owner.controller, loc = loc, orientation = orientation, faction = owner.fraction,
         image = images[0], radius = radius, rotate_image = True, properties = properties)
        self.images = images
        self.flip_num = 0

    def update(self):
        self.flip_num += 1
        if self.flip_num >= len(self.images):
            self.flip_num = 0
        self.origional_image = self.images[self.flip_num]
        super().update()