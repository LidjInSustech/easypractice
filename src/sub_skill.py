import pygame as pg
import math
import entities
import effects

def magis_requirement(owner, value):
    if owner.magis_point >= value:
        owner.magis_point -= value
        return True
    else:
        return False

class fast_forward(entities.Visible):
    def __init__(self, owner, picture, speed, image_invincible, image_unstable):
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

        owner.effects.append(effects.icon("invincible", 4, image_invincible))
        owner.effects.append(effects.simple_forward(owner, speed))
        owner.effects.append(effects.icon("unstable", 12, image_unstable))

    def update(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.core.spaces.remove(self)

class fast_slide(entities.Visible):
    def __init__(self, owner, picture, speed, image_invincible, image_unstable):
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

        owner.effects.append(effects.icon("invincible", 4, image_invincible))
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

class magic_sperm(entities.Entity):
    def __init__(self, owner, orient, images):
        if not magis_requirement(owner, 10):
            return
        if any([e.eid == 'magic_sperm_cd' for e in owner.effects]):
            return
        owner.effects.append(effects.effect('magic_sperm_cd', 10))
        x = math.cos(math.radians(orient))*owner.size*1.2 + owner.loc_x
        y = math.sin(math.radians(orient))*owner.size*1.2 + owner.loc_y
        super().__init__(owner.core, x, y, orient, images[0])
        self.owner = owner
        self.images = images
        self.image = self.images[0]
        self.life = 60
        self.core = owner.core
        self.core.entities.add(self)

        self.health_point = 10
        self.max_hp = 10
        self.party = owner.party
        self.size = 8
        self.damage_range = 12
        self.damage = 10

    def update(self):
        if self.life > 0:
            self.life -= 1
            self.ori_image = self.images[self.life%len(self.images)]
            self.effects.append(effects.simple_forward(self, self.speed))
            super().update()
            for entity in self.core.entities:
                if entity.party != self.party:
                    if (self.loc_x-entity.loc_x)**2 + (self.loc_y-entity.loc_y)**2 < (self.damage_range+entity.size)**2:
                        entity.demage(self.damage)
                        self.core.entities.remove(self)
                        self.life = 0
        else:
            self.core.entities.remove(self)

class slow_cut(entities.Visible):
    def __init__(self, owner, orient, images, unmovable_image, size):
        time = 16
        if any([e.eid == 'slow_cut_cd' for e in owner.effects]):
            return
        owner.effects.append(effects.effect('slow_cut_cd', time+1))
        owner.effects.append(effects.icon("unmovable", time, unmovable_image))
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, orient)
        self.owner = owner
        self.images = images
        self.image = self.images[0]
        x, y, orient = self.absolute_location()
        self.image = pg.transform.rotate(self.image, orient-90)
        self.rect = self.image.get_rect(center=(x, y))
        self.core = owner.core
        self.core.spaces.add(self)

        self.life = time
        self.party = owner.party
        self.damage_range = size//2
        self.damage = 20

    def update(self):
        self.life -= 1
        x, y, orient = self.absolute_location()
        self.rect = self.image.get_rect(center=(x, y))
        if self.life < 0:
            self.core.spaces.remove(self)
        elif self.life == 3:
            image = self.images[0].copy()
            image.blit(self.images[1], (0,0))
            self.image = pg.transform.rotate(image, orient-90)
            super().update()
        elif self.life == 2:
            image = self.images[0].copy()
            image.blit(self.images[2], (0,0))
            self.image = pg.transform.rotate(image, orient-90)
            super().update()
            for entity in self.core.entities:
                if entity.party != self.party:
                    ori1 = math.degrees(math.atan2(entity.loc_y-self.loc_y, entity.loc_x-self.loc_x))
                    if (ori1 - self.orient)%360 < 60 or (ori1 - self.orient)%360 > 300:
                        if (entity.loc_x-self.loc_x)**2+(entity.loc_y-self.loc_y)**2 < (self.damage_range+entity.size)**2:
                            entity.demage(self.damage)
        else:
            super().update()