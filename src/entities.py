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
        self.update()

    def calculate_position(self):
        if self.camera is None:
            raise Exception('Camera is not set')
        self.draw_pos = self.loc - self.camera.loc
        self.draw_pos.rotate_ip(-self.camera.orient)
        self.draw_pos += self.camera.center
        self.draw_orient = self.orientation - self.camera.orient

    def handle_image(self, source_image):
        self.calculate_position()
        if self.rotate_image:
            self.image = pg.transform.rotate(source_image, self.draw_orient)
        else:
            self.image = source_image
        self.rect = self.image.get_rect(center=self.draw_pos)

    def update(self):
        self.handle_image(origional_image)

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
        if 'max_hp' not in properties:
            properties['max_hp'] = 1000
        if 'hp' not in properties:
            properties['hp'] = properties['max_hp']
        if 'max_mp' not in properties:
            properties['max_mp'] = 1000
        if 'mp' not in properties:
            properties['mp'] = properties['max_mp']
        if 'mp_regen' not in properties:
            properties['mp_regen'] = 0
        self.properties = properties
        self.effects = []

    def update(self):
        self.effect = filter(lambda x: x.update(), self.effects)
        self.properties['mp'] += self.properties['mp_regen']
        self.properties['mp'] = min(self.properties['mp'], self.properties['max_mp'])
        self.properties['hp'] = min(self.properties['hp'], self.properties['max_hp'])
        if self.properties['hp'] <= 0:
            self.kill()
        else:
            super().update()

class Movable(Entity):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, mask_surface = None, rotate_image = True, properties = None):
        super().__init__(controller, loc, orientation, faction, image, mask_surface, rotate_image, properties)
        if 'speed' not in self.properties:
            self.properties['speed'] = 5

    def move(relative_direction, distance):
        colisions = []
        for entity in self.controller.entities:
            if entity.faction != self.faction and pg.sprite.collide_mask(self, entity):
                colisions.append(entity)
        move_vector = pg.math.Vector2.from_polar((distance, self.orientation + relative_direction))
        self.loc += move_vector
        for entity in self.controller.entities:
            if entity.faction != self.faction and pg.sprite.collide_mask(self, entity) and entity not in colisions:
                self.loc -= move_vector
                break