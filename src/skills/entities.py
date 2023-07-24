import pygame as pg
import visibles

class Fliping(visibles.Movable):
    def __init__(self, owner, loc = pg.math.Vector2(), orientation = 0, images = None, radius = None, properties = None):
        super().__init__(owner.controller, loc = loc, orientation = orientation, faction = owner.faction,
         image = images[0], radius = radius, rotate_image = True, properties = properties)
        self.images = images
        self.flip_num = 0

    def update(self):
        self.flip_num += 1
        if self.flip_num >= len(self.images):
            self.flip_num = 0
        self.origional_image = self.images[self.flip_num]
        super().update()

class MagicBullet(Fliping):
    def __init__(self, owner, images, loc = pg.math.Vector2(), orientation = 0, properties = None):
        if properties is None:
            properties = {'max_hp': 100, 'max_mp':0, 'mp_regen':0, 'speed': 5, 'size': 10, 'life': 100}
        super().__init__(owner, loc = loc, orientation = orientation, images = images, radius = properties['size']/2, properties = properties)
        self.properties = properties
        self.life = properties['life']

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
        self.move()
        super().update()