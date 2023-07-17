import pygame as pg
import math
import entities
import effects

class fast_forward(entities.Visible):
    def __init__(self, owner, picture, speed, image_escaping, image_unstable):
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, owner.orient)
        self.owner = owner
        self.speed = speed
        x, y, orient = self.absolute_location()
        self.image = pg.transform.scale(picture, (abs(speed)*2, abs(speed)*2))
        if speed < 0:
            self.image = pg.transform.rotate(self.image, orient+180)
        else:
            self.image = pg.transform.rotate(self.image, orient)
        self.rect = self.image.get_rect(center=(x, y))
        self.life = 2
        self.core = owner.core
        self.core.spaces.add(self)

        owner.effects.append(effects.icon("escaping", 4, image_escaping))
        owner.effects.append(effects.simple_forward(owner, speed))
        owner.effects.append(effects.icon("unstable", 12, image_unstable))

    def update(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.core.spaces.remove(self)

class fast_slide(entities.Visible):
    def __init__(self, owner, picture, speed, image_escaping, image_unstable):
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, owner.orient)
        self.owner = owner
        self.speed = speed
        x, y, orient = self.absolute_location()
        self.image = pg.transform.scale(picture, (abs(speed)*2, abs(speed)*2))
        if speed < 0:
            self.image = pg.transform.rotate(self.image, orient+90)
        else:
            self.image = pg.transform.rotate(self.image, orient-90)
        #self.image = pg.transform.rotate(self.image, orient)
        self.rect = self.image.get_rect(center=(x, y))
        self.life = 2
        self.core = owner.core
        self.core.spaces.add(self)

        owner.effects.append(effects.icon("escaping", 4, image_escaping))
        owner.effects.append(effects.simple_slide(owner, speed))
        owner.effects.append(effects.icon("unstable", 10, image_unstable))

    def update(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.core.spaces.remove(self)

class fast_turn():
    def __init__(self, owner, angle):
        owner.effects.append(effects.simple_turn(owner, angle))