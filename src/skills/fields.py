import pygame as pg
import math
import visibles

class Field(visibles.Visible):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, faction = 0, image = None, rotate_image = True):
        self.controller = controller
        self.faction = faction
        super().__init__(controller.camera, loc, orientation, image, rotate_image)

    def touch(self, entity):
        return False

class AccessoryField(Field):
    def __init__(self, owner, drift = None, orient_drift = 0, image = None, rotate_image = True):
        super().__init__(owner.controller, owner.loc, owner.orientation, owner.faction, image, rotate_image)
        self.owner = owner
        self.drift = drift
        self.orient_drift = orient_drift

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
        self.orientation = self.owner.orientation + self.orient_drift

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
        self.knockback = properties.get('knockback', 0)
        super().__init__(owner, drift = pg.math.Vector2(2*properties.get('extension', 1.1), 0), image = image)

    def update(self):
        super().update()
        for e in self.controller.entities:
            if self.touch(e):
                e.damage(self.attack)
                e.passive_move(direction = self.orientation, distance = self.knockback)
                self.owner.kill()
                self.kill()

    def touch(self, entity):
        if entity.faction != self.faction:
            return (entity.loc - self.loc).length_squared() <= (entity.radius + self.radius)**2
        return False

class Cut(AccessoryField):
    def __init__(self, owner, orient_drift, images, properties = None, side = False):
        self.properties = properties
        self.side = side
        self.radius = properties.get('size', 128)*properties.get('extension', 1)
        self.attack = properties.get('attack', 100)
        self.life = properties.get('duration', 5) + properties.get('before', 0)
        self.life = max(self.life, 5)
        self.images = images
        self.owner = owner
        super().__init__(owner, drift = None, orient_drift = orient_drift, image = images[0], rotate_image = True)
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
                    return True
        return False

class Lunge(AccessoryField):
    def __init__(self, owner, orient_drift, images, properties = None, dash = 0):
        self.properties = properties
        self.dash = dash
        self.radius = properties.get('size', 64)*properties.get('extension', 1)
        self.attack = properties.get('attack', 100)
        self.life = properties.get('before', 0) + properties.get('duration', 5)
        self.life = max(self.life, 5)
        self.images = images
        self.owner = owner
        image = images[0] if dash == 0 else images[3]
        super().__init__(owner, drift = pg.Vector2.from_polar((self.radius, orient_drift)), orient_drift = orient_drift, image = image, rotate_image = True)
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
            
            if self.dash != 0:
                self.owner.passive_move(direction = self.orientation, distance = self.dash)
            super().update()

            for entities in self.controller.entities:
                if self.touch(entities):
                    entities.damage(self.attack)

    def touch(self, entity):
        if entity.faction != self.faction:
            base = pg.math.Vector2.from_polar((1, self.orientation))
            vector = entity.loc - self.loc
            if abs(base.cross(vector)) < self.radius/2 + entity.radius:
                if abs(base.dot(vector)) < self.radius + entity.radius:
                    return True
        return False

class FireBall(MagicBullet):
    def __init__(self, owner, image, explode_image, properties = None):
        self.explode_image = explode_image
        self.properties = properties
        self.radius = properties.get('size', 32)*properties.get('extension', 1.1)
        self.attack = properties.get('attack', 50)
        super().__init__(owner, image, properties)

    def update(self):
        super().update()
        if not self.owner.alive:
            explode = FireBallExplode(self, self.explode_image, self.properties)
            self.controller.fields.add(explode)
            explode.update()

class FireBallExplode(Field):
    def __init__(self, owner, image, properties = None):
        self.properties = properties
        self.radius = properties.get('size2', 64)*properties.get('extension', 1.1)
        self.attack = properties.get('attack2', 200)
        self.life = 5
        super().__init__(owner.controller, loc = owner.loc, orientation = 0, faction = owner.faction, image = image, rotate_image = False)

    def update(self):
        if self.life == 5:
            for e in self.controller.entities:
                if self.touch(e):
                    e.damage(self.attack)
        self.life -= 1
        if self.life <= 0:
            self.kill()
        super().update()

    def touch(self, entity):
        if entity.faction != self.faction:
            return (entity.loc - self.loc).length_squared() <= (entity.radius + self.radius)**2
        return False

class HelixCut(AccessoryField):
    def __init__(self, owner, image, properties = None):
        self.radius = properties.get('size', 64)*properties.get('extension', 1)
        self.count = 3
        self.damaged = []
        super().__init__(owner, drift = None, orient_drift = 0, image = image, rotate_image = True)
    
    def update(self):
        self.count = (self.count + 1)%3
        if self.count == 0:
            self.orient_drift = (self.orient_drift + 90)%360
            self.damaged = []
        super().update()
        for e in self.controller.entities:
            if self.touch(e):
                self.damaged.append(e)
                e.damage(100)
    
    def touch(self, entity):
        if entity in self.damaged:
            return False
        angles = (45, 315)
        if entity.faction != self.faction:
            vector = entity.loc - self.loc
            if vector.length_squared() <= (entity.radius + self.radius)**2:
                r, phi = vector.as_polar()
                if (phi - self.orientation)%360 < angles[0] or (phi - self.orientation)%360 > angles[1]:
                    return True
        return False

class Laser(Field):
    def __init__(self, owner, orient_drift, properties = None):
        super().__init__(owner.controller, loc = owner.loc, orientation = owner.orientation + orient_drift, faction = owner.faction, image = 'red')
        self.owner = owner
        self.properties = properties
        self.width = properties.get('size', 2)*properties.get('extension', 1)
        self.attack = properties.get('attack', 100)
        self.representation = pg.math.Vector2.from_polar((1, owner.orientation + orient_drift))
        self.length = self.get_length()
        self.handle_image()
        self.life = 6

    def update(self):
        self.life -= 1
        if self.life < 0:
            self.kill()
        elif self.life > 2:
            return
        elif self.life == 2:
            self.origional_image = 'white'
            for e in self.controller.entities:
                if self.touch(e):
                    e.damage(self.attack)
        self.loc = self.owner.loc
        self.length = self.get_length()
        super().update()

    def handle_image(self):
        source_image = self.origional_image
        length = self.length
        self.calculate_position()
        draw_orient = self.draw_orient
        image_vector = pg.math.Vector2.from_polar((length, draw_orient))

        image = pg.Surface((abs(image_vector.y)+self.width, abs(image_vector.x)+self.width))
        rect = image.get_rect()
        image.set_colorkey((0,0,0))
        if source_image == 'red':
            image.set_alpha(80)
            color = (255,0,0)
        else:
            color = (255,255,255)
        draw_orient = draw_orient%180
        if draw_orient < 90:
            pg.draw.line(image, color, (0,0), rect.size, self.width*2)
        else:
            pg.draw.line(image, color, (0,rect.height), (rect.width,0), self.width*2)
        self.image = image

        draw_orient = self.draw_orient%360
        if draw_orient > 180:
            rect.left = self.draw_pos.x
        else:
            rect.right = self.draw_pos.x
        if draw_orient > 90 and draw_orient < 270:
            rect.top = self.draw_pos.y
        else:
            rect.bottom = self.draw_pos.y
        self.rect = rect

    def touch(self, entity):
        if entity.faction != self.faction:
            base = self.representation
            vector = entity.loc - self.loc
            if abs(base.cross(vector)) < self.width/2 + entity.radius:
                dot = base.dot(vector)
                if dot < self.length + entity.radius + 1 and dot > 0:
                    return True
        return False

    def get_length(self):
        representation = self.representation
        loc = self.loc
        min_length = self.boundary_length()
        for e in self.controller.entities:
            if e.faction != self.faction:
                vector = e.loc - self.loc
                if abs(representation.cross(vector)) < self.width/2 + e.radius:
                    length = representation.dot(vector)
                    if length > 0:
                        min_length = min(min_length, length)
        return min_length

    def boundary_length(self):
        representation = self.representation
        loc = self.loc
        if representation.x >= 0:
            x_length = self.controller.boundary.x - loc.x
        elif representation.x < 0:
            x_length = self.controller.boundary.x + loc.x
        if representation.y >= 0:
            y_length = self.controller.boundary.y - loc.y
        elif representation.y < 0:
            y_length = self.controller.boundary.y + loc.y
        eps = 1e-6
        return min(x_length/(abs(representation.x)+eps), y_length/(abs(representation.y)+eps))