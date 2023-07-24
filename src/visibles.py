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
    def __init__(self, owner, drift = None, image = None, rotate_image = True):
        super().__init__(owner.camera, owner.loc, owner.orientation, image, rotate_image)
        self.owner = owner
        self.drift = drift

    def update(self):
        if not self.owner.alive:
            self.kill()
        self.update_location()
        super().update()

    def update_location(self):
        if self.drift is not None and self.rotate_image:
                self.loc = self.owner.loc + self.drift.rotate(self.owner.orientation)
        else:
            self.loc = self.owner.loc
        self.orientation = self.owner.orientation

    def calculate_position(self):
        super().calculate_position()
        if self.drift is not None and not self.rotate_image:
            self.draw_pos += self.drift
        
class Entity(Visible):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, radius = None, rotate_image = True, properties = None):
        self.controller = controller
        self.faction = faction
        super().__init__(controller.camera, loc, orientation, image, rotate_image)
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

        if radius is None:
            radius = image.get_width()/2
        self.radius = radius
        self.alive = True

    def update(self):
        self.effects = list(filter(lambda x: x.update(), self.effects))
        self.mp += self.mp_regen
        self.mp = min(self.mp, self.max_mp)
        self.hp = min(self.hp, self.max_hp)
        if self.hp <= 0:
            self.kill()
        else:
            super().update()

    def kill(self):
        self.alive = False
        super().kill()

class Movable(Entity):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, radius = None, rotate_image = False, properties = None):
        super().__init__(controller, loc, orientation, faction, image, radius, rotate_image, properties)

    def move(self, relative_direction = 0, distance = None):
        if distance is None:
            distance = self.speed
        collision = []
        for entity in self.controller.entities:
            if entity.faction != self.faction and entity.colliding(self):
                collision.append(entity)
        self.attampt_move(collision, relative_direction, distance)
        
    def colliding(self, other):
        return self.loc.distance_squared_to(other.loc) < (self.radius + other.radius)**2
    
    def attampt_move(self, collisions, relative_direction, distance):
        move_vector = pg.math.Vector2.from_polar((distance, self.orientation + relative_direction))
        self.loc += move_vector
        for entity in self.controller.entities:
            if entity.faction != self.faction and entity.colliding(self) and entity not in collisions:
                self.loc -= move_vector
                if distance > 2:
                    self.attampt_move(collisions, relative_direction, distance/2)