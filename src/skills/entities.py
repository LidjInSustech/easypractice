import pygame as pg
import visibles
import automixin

class Fliping(visibles.Movable):
    def __init__(self, owner, loc = pg.math.Vector2(), orientation = 0, images = None, radius = None, properties = None):
        super().__init__(owner.controller, loc = loc, orientation = orientation, faction = owner.faction,
         image = images[0], radius = radius, rotate_image = True, properties = properties)
        self.images = images
        self.flip_num = 0
        self.handle_image()

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
        self.edge = False

    def update(self):
        self.life -= 1
        if self.life <= 0 or self.edge:
            self.kill()
        self.move()
        super().update()

class Missile(Fliping, automixin.Missile):
    def __init__(self, owner, images, loc = pg.math.Vector2(), orientation = 0, properties = None):
        radius = properties.get('size', 32)
        super().__init__(owner, loc = loc, orientation = orientation, images = images, radius = radius, properties = properties)
        self.life = properties.get('life', 200)
        self.edge = False

    def update(self):
        self.life -= 1
        if self.life <= 0 or self.edge:
            self.kill()
        self.auto()
        self.move()
        super().update()

    def auto(self):
        min_distance = self.properties['sense']**2
        min_destination = None
        for e in self.controller.entities:
            if e.faction != self.faction:
                vector = e.loc - self.loc
                distance = vector.length_squared()
                if distance < min_distance:
                    min_distance = distance
                    min_destination = e.loc
        if min_destination is not None:
            self.navigate(min_destination)

class Billiard(MagicBullet):
    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
        self.bounce()
        self.move()
        super().update()

    def bounce(self):
        if abs(self.loc.x) >= self.controller.boundary.x:
            self.orientation = 180 - self.orientation
        if abs(self.loc.y) >= self.controller.boundary.y:
            self.orientation = -self.orientation

    def bounce_(self, entity):
        vector = entity.loc - self.loc
        polar = vector.as_polar()[1] + 90
        self.orientation = (2*polar - self.orientation)%360

class Bubble(visibles.Movable):
    def __init__(self, owner, orientation = 0, image = None, properties = None):
        self.life = properties.get('life', 100)
        self.radius = properties.get('size', 32)
        super().__init__(owner.controller, loc = owner.loc.copy(), orientation = orientation, faction = owner.faction,
         image = image, radius = self.radius, rotate_image = False, properties = properties.copy())
        self.handle_image()

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
        if self.life%4 == 0:
            if self.properties['speed'] > 0:
                self.properties['speed'] -= 1
        self.move()
        super().update()

class StoneColumn(visibles.Stationary):
    def __init__(self, owner, drift, image, properties = None):
        self.radius = properties.get('size', 32)
        loc = owner.loc + drift.rotate(owner.orientation)
        super().__init__(owner.controller, loc = loc, orientation = 0, faction = owner.faction,
         image = image, radius = self.radius, rotate_image = False, properties = properties)
        self.handle_image()

