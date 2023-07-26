import pygame as pg
import visibles

class Field(visibles.Visible):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, rotate_image = True):
        self.controller = controller
        self.faction = faction
        super().__init__(controller.camera, loc, orientation, image, rotate_image)

    def touch(self, entity):
        return False

class AccessoryField(Field):
    def __init__(self, owner, drift = None, image = None, rotate_image = True):
        super().__init__(owner.controller, owner.loc, owner.orientation, owner.faction, image, rotate_image)
        self.owner = owner
        self.drift = drift

    def update(self):
        if not self.owner.alive:
            self.kill()
        self.update_location()
        super().update()

    def update_location(self):
        if self.drift is not None:
            if self.rotate_image:
                self.loc = self.owner.loc + self.drift.rotate(self.owner.orientation)
            else:
                self.loc = self.owner.loc + self.drift
        else:
            self.loc = self.owner.loc
        self.orientation = self.owner.orientation

class FastMove(Field):
    def __init__(self, owner, orientation, image, life_time = 4):
        self.life_time = life_time
        super().__init__(owner.controller, loc = owner.loc, orientation = orientation, faction = owner.faction, image = image, rotate_image = True)

    def update(self):
        self.life_time -= 1
        if self.life_time <= 0:
            self.kill()
        super().update()

class MagicBullet(AccessoryField):
    def __init__(self, owner, image, properties = None):
        self.properties = properties
        self.radius = properties.get('size', 32)*properties.get('extension', 1.1)
        self.attack = properties.get('attack', 100)
        super().__init__(owner, drift = pg.math.Vector2(2*properties.get('extension', 1.1), 0), image = image)

    def update(self):
        super().update()
        for entities in self.controller.entities:
            if entities.faction != self.faction:
                if self.touch(entities):
                    entities.damage(self.attack)
                    self.owner.kill()

    def touch(self, entity):
        return (entity.loc - self.loc).length_squared() <= (entity.radius + self.radius)**2

class Cut(Field):
    def __init__(self, owner, loc, orientation, images, properties = None, side = False):
        self.properties = properties
        self.side = side
        self.radius = properties.get('size', 128)*properties.get('extension', 1)
        self.attack = properties.get('attack', 100)
        self.life = properties.get('base_cd', 10)
        self.life = max(self.life, 5)
        self.images = images
        self.owner = owner
        super().__init__(owner.controller, loc = loc, orientation = orientation, faction = owner.faction, image = images[0], rotate_image = True)
        super().update()

    def update(self):
        self.life -= 1
        if self.life < 0:
            self.kill()
        elif self.life == 4:
            self.origional_image = self.images[0].copy()
            self.origional_image.blit(self.images[1], (0,0))
            super().update()
        elif self.life == 2:
            self.origional_image = self.images[0].copy()
            self.origional_image.blit(self.images[2], (0,0))
            super().update()
            
            if self.side:
                self.owner.orientation = self.orientation

            for entities in self.controller.entities:
                if entities.faction != self.faction:
                    if self.touch(entities):
                        entities.damage(self.attack)

    def touch(self, entity):
        if self.side:
            angles = (90, 270)
        else:
            angles = (60, 300)

        if entity.faction != self.faction:
            vector = entity.loc - self.loc
            if vector.length_squared() <= (entity.radius + self.radius)**2:
                r, phi = vector.as_polar()
                if (phi - self.orientation)%360 < angles[0] or (phi - self.orientation)%360 > angles[1]:
                    entity.damage(self.attack)