import pygame as pg
import math
import util

class Visible(pg.sprite.Sprite):
    def __init__(self, camera, loc = pg.math.Vector2(), orientation = 0, image = None, rotate_image = True):
        super().__init__()
        self.camera = camera
        self.loc = loc
        self.orientation = orientation
        self.origional_image = image
        self.rotate_image = rotate_image

    def calculate_position(self):
        if self.camera is None:
            raise Exception('Camera is not set')
        self.draw_pos = self.loc - self.camera.loc
        self.draw_pos.rotate_ip(-self.camera.orientation-90)
        self.draw_pos.reflect_ip(pg.math.Vector2(1,0))
        self.draw_pos += self.camera.center
        self.draw_orient = self.orientation - self.camera.orientation

    def handle_image(self, source_image):
        self.calculate_position()
        if self.rotate_image:
            self.image = pg.transform.rotate(source_image, self.draw_orient)
        else:
            self.image = source_image
        self.rect = self.image.get_rect(center=self.draw_pos)

    def update(self):
        self.handle_image(self.origional_image)
        super().update()

class Accessory(Visible):
    def __init__(self, camera, owner, image = None, rotate_image = True):
        super().__init__(camera, owner.loc, owner.orientation, image, rotate_image)

    def update(self):
        self.loc = self.owner.loc
        self.orientation = self.owner.orientation
        super().update()

class Field(Visible):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, mask_surface = None, rotate_image = True):
        self.original_mask = mask_surface
        self.controller = controller
        self.faction = faction
        super().__init__(controller.camera, loc, orientation, image, rotate_image)

    def update_mask(self):
        if self.original_mask is None:
            self.mask = pg.mask.from_surface(self.image)
        else:
            if self.rotate_image:
                self.mask = pg.mask.from_surface(pg.transform.rotate(self.original_mask, self.draw_orient))
            else:
                self.mask = pg.mask.from_surface(self.original_mask)

    def handle_image(self, source_image):
        self.calculate_position()
        if self.rotate_image:
            self.image = pg.transform.rotate(source_image, self.draw_orient)
        else:
            self.image = source_image
        self.rect = self.image.get_rect(center=self.draw_pos)
        self.update_mask()
        
class Entity(Field):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, mask_surface = None, rotate_image = True, properties = None):
        super().__init__(controller, loc, orientation, faction, image, mask_surface, rotate_image)
        if properties is None:
            properties = {}
        if 'max_hp' not in properties:
            properties['max_hp'] = 1000
        if 'max_mp' not in properties:
            properties['max_mp'] = 1000
        if 'mp_regen' not in properties:
            properties['mp_regen'] = 0
        if 'speed' not in properties:
            properties['speed'] = 5
        
        self.max_hp = properties['max_hp']
        self.max_mp = properties['max_mp']
        self.mp_regen = properties['mp_regen']
        self.speed = properties['speed']
        self.hp = self.max_hp
        self.mp = self.max_mp

        self.properties = properties
        self.effects = []

    def update(self):
        self.effects = filter(lambda x: x.update(), self.effects)
        self.mp += self.mp_regen
        self.mp = min(self.mp, self.max_mp)
        self.hp = min(self.hp, self.max_hp)
        if self.hp <= 0:
            self.kill()
        else:
            super().update()

class Movable(Entity):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, mask_surface = None, rotate_image = True, properties = None):
        super().__init__(controller, loc, orientation, faction, image, mask_surface, rotate_image, properties)
        self.colisions = []
        self.last_loc = self.loc.copy()
        self.handle_image(self.origional_image)

    def move(self, relative_direction = 0, distance = None):
        if distance is None:
            distance = self.speed
        move_vector = pg.math.Vector2.from_polar((distance, self.orientation + relative_direction))
        self.loc += move_vector

    def update(self):
        super().update()
        colisions = []
        for entitiy in self.controller.entities:
            if entitiy.faction != self.faction:
                if pg.sprite.collide_mask(self, entitiy):
                    colisions.append(entitiy)
        if len(colisions) <= len(self.colisions):
            self.colisions = colisions
            self.last_loc = self.loc.copy()
        else:
            self.loc = self.last_loc
        