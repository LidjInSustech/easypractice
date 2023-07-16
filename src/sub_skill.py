import pygame as pg
import math
import entities
import effects

class fast_forward(entities.Visible):
    def __init__(self, owner, picture, speed):
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, owner.orient)
        self.owner = owner
        self.speed = speed
        x, y, orient = self.absolute_location()
        self.image = pg.transform.scale(picture, (abs(speed)*3, abs(speed)*3))
        self.image = pg.transform.rotate(self.image, orient)
        self.rect = self.image.get_rect(center=(x, y))
        self.life = 2
        self.core = owner.core
        self.core.spaces.add(self)

        owner.effects.append(effects.escaping(4))
        owner.effects.append(effects.simple_forward(owner, speed))
        owner.effects.append(effects.unstable(10))

    def update(self):
        if self.life == 2:
            self.life = 1
            self.owner.effects.append(effects.simple_forward(self.owner, self.speed))
        elif self.life == 1:
            self.life = 0
        else:
            self.core.spaces.remove(self)
