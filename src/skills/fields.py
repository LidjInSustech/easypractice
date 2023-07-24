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
        if properties is None:
            properties = {'size': 10, 'extension': 4, 'damage': 100}
        extension = properties['extension']
        super().__init__(owner, drift = pg.math.Vector2(2+extension/2, 0), image = image)
        self.properties = properties
        self.size = properties['size']
        self.radius = self.size/2
        self.damage = properties['damage']

    def update(self):
        super().update()
        for entities in self.controller.entities:
            if entities.faction != self.faction:
                if self.touch(entities):
                    entities.hp -= self.damage
                    self.owner.kill()


    def touch(self, entity):
        return (entity.loc - self.loc).length_squared() <= (entity.radius + self.radius)**2