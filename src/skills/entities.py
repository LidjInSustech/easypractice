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
        radius = properties.get('size', 32)
        super().__init__(owner, loc = loc, orientation = orientation, images = images, radius = radius, properties = properties)
        self.life = properties.get('life', 100)

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
        self.move()
        super().update()

class Missile(Fliping):
    def __init__(self, owner, images, loc = pg.math.Vector2(), orientation = 0, properties = None):
        radius = properties.get('size', 32)
        super().__init__(owner, loc = loc, orientation = orientation, images = images, radius = radius, properties = properties)
        self.life = properties.get('life', 200)

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
        self.auto()
        self.move()
        super().update()

    def auto(self):
        for e in self.controller.entities:
            if e.faction != self.faction:
                vector = e.loc - self.loc
                if vector.length_squared() <= self.properties['sense']**2:
                    polar = (vector.as_polar()[1] - self.orientation)%360
                    if polar > self.properties['turn'] and polar < 360-self.properties['turn']:
                        if polar > 180:
                            self.orientation -= self.properties['turn']
                        else:
                            self.orientation += self.properties['turn']

                    