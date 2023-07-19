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
    def __init__(self, owner, orient, picture, speed, image_invincible, image_unstable):
        for effect in owner.effects:
            if effect.eid in ("unmovable", "unstable"):
                return
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, orient)
        self.owner = owner
        x, y, orient = self.absolute_location()
        self.image = pg.transform.scale(picture, (speed*2, speed*2))
        self.image = pg.transform.rotate(self.image, orient)
        self.rect = self.image.get_rect(center=(x, y))
        self.life = 2
        self.core = owner.core
        self.core.spaces.add(self)

        owner.effects.append(effects.icon("invincible", 4, image_invincible))
        owner.effects.append(effects.icon("unstable", 12, image_unstable))
        owner.loc_x += speed * math.cos(math.radians(self.orient))
        owner.loc_y += speed * math.sin(math.radians(self.orient))

    def update(self):
        if self.life > 0:
            self.life -= 1
        else:
            self.core.spaces.remove(self)

class fast_turn():
    def __init__(self, owner, angle):
        for effect in owner.effects:
            if effect.eid == "unmovable":
                return
        owner.orient += angle

class magic_sperm(entities.Entity):
    def __init__(self, owner, orient, images):
        if not magis_requirement(owner, 100):
            return
        if any([e.eid == 'magic_sperm_cd' for e in owner.effects]):
            return
        owner.effects.append(effects.effect('magic_sperm_cd', 10))
        #x = math.cos(math.radians(orient))*owner.size*1.2 + owner.loc_x
        #y = math.sin(math.radians(orient))*owner.size*1.2 + owner.loc_y
        #super().__init__(owner.core, x, y, orient, images[0])
        super().__init__(owner.core, owner.loc_x, owner.loc_y, orient, images[0])
        self.owner = owner
        self.images = images
        self.image = self.images[0]
        self.life = 60
        self.core = owner.core
        self.core.entities.add(self)

        self.health_point = 100
        self.max_hp = 100
        self.party = owner.party
        self.size = 8
        self.damage_range = 14
        self.damage = 80
        self.update()

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
    def __init__(self, owner, orient, images, unmovable_image, size, slow = True, side = False):
        if slow:
            time = 16
        else:
            time = 4
        if any([e.eid == 'sword_cd' for e in owner.effects]):
            return
        owner.effects.append(effects.effect('sword_cd', time+1))
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
        if slow:
            self.damage = 200
        else:
            self.damage = 50
        self.side = side

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

            if self.side:
                angles = (90, 270)
                self.owner.orient = self.orient
            else:
                angles = (60, 300)

            for entity in self.core.entities:
                if entity.party != self.party:
                    ori1 = math.degrees(math.atan2(entity.loc_y-self.loc_y, entity.loc_x-self.loc_x))
                    if (ori1 - self.orient)%360 < angles[0] or (ori1 - self.orient)%360 > angles[1]:
                        if (entity.loc_x-self.loc_x)**2+(entity.loc_y-self.loc_y)**2 < (self.damage_range+entity.size)**2:
                            entity.demage(self.damage)
        else:
            super().update()

class missile(entities.Entity):
    def __init__(self, owner, orient, images):
        if not magis_requirement(owner, 200):
            return
        if any([e.eid == 'missile_cd' for e in owner.effects]):
            return
        owner.effects.append(effects.effect('missile_cd', 10))
        super().__init__(owner.core, owner.loc_x, owner.loc_y, orient, images[0])
        self.owner = owner
        self.images = images
        self.ori_image = self.images[0]
        self.life = 400
        self.core = owner.core
        self.core.entities.add(self)

        self.health_point = 80
        self.max_hp = 80
        self.party = owner.party
        self.size = 18
        self.damage_range = 24
        self.damage = 80
        self.update()

    def update(self):
        if self.life > 0:
            self.life -= 1
            self.ori_image = self.images[self.life%len(self.images)]
            self.move()
            super().update()
            for entity in self.core.entities:
                if entity.party != self.party:
                    if (self.loc_x-entity.loc_x)**2 + (self.loc_y-entity.loc_y)**2 < (self.damage_range+entity.size)**2:
                        entity.demage(self.damage)
                        self.core.entities.remove(self)
                        self.life = 0
        else:
            self.core.entities.remove(self)

    def move(self):
        minimum = 40000
        target = None
        for e in self.core.entities:
            if e.party != self.party:
                distance = (self.loc_x-e.loc_x)**2 + (self.loc_y-e.loc_y)**2
                if minimum is None or distance < minimum:
                    minimum = distance
                    target = e
        if target is not None:
            target_orient = math.degrees(math.atan2(target.loc_y-self.loc_y, target.loc_x-self.loc_x))
            target_orient = (target_orient - self.orient)%360
            if target_orient > 180:
                self.effects.append(effects.simple_turn(self, -4))
            else:
                self.effects.append(effects.simple_turn(self, 4))
        self.effects.append(effects.simple_forward(self, 5))
                

class fireball(entities.Entity):
    def __init__(self, owner, orient, images, image_final, size1, size2):
        if not magis_requirement(owner, 200):
            return
        if any([e.eid == 'fireball_cd' for e in owner.effects]):
            return
        owner.effects.append(effects.effect('fireball_cd', 10))
        super().__init__(owner.core, owner.loc_x, owner.loc_y, orient, images[0])
        self.owner = owner
        self.images = images
        self.image = self.images[0]
        self.image_final = image_final
        self.core = owner.core
        self.core.entities.add(self)

        self.health_point = 100
        self.max_hp = 100
        self.life = self.health_point
        self.party = owner.party
        self.size = size1
        self.size2 = size2
        self.damage_range = size1 + 5
        self.damage = 20
        self.update()

    def update(self):
        self.health_point -= 1
        self.life = self.health_point
        if self.health_point <= 0:
            fireball_final(self, self.image_final, self.size2)
        self.ori_image = self.images[self.life%len(self.images)]
        self.effects.append(effects.simple_forward(self, self.speed))
        super().update()
        for entity in self.core.entities:
            if entity.party != self.party:
                if (self.loc_x-entity.loc_x)**2 + (self.loc_y-entity.loc_y)**2 < (self.damage_range+entity.size)**2:
                    entity.demage(self.damage)
                    self.core.entities.remove(self)
                    fireball_final(self, self.image_final, self.size2)

class fireball_final(entities.Visible):
    def __init__(self, owner, image, size):
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, owner.orient)
        self.owner = owner
        self.image = image
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.core = owner.core
        self.core.spaces.add(self)

        self.life = 4
        self.party = owner.party
        self.damage_range = size
        self.damage = 200

        x, y, orient = self.absolute_location()
        self.rect = self.image.get_rect(center=(x, y))

        for entity in self.core.entities:
            if entity.party != self.party:
                if (self.loc_x-entity.loc_x)**2 + (self.loc_y-entity.loc_y)**2 < (self.damage_range+entity.size)**2:
                    entity.demage(self.damage)

    def update(self):
        self.life -= 1
        x, y, orient = self.absolute_location()
        self.rect = self.image.get_rect(center=(x, y))
        if self.life < 0:
            self.core.spaces.remove(self)
        super().update()

class helix_cut(entities.Visible):
    def __init__(self, owner, image, size, image_unstable):
        if any([e.eid in ('sword_cd', 'unmovable', 'unstable') for e in owner.effects]):
            return
        self.effect1 = effects.effect('sword_cd', -1)
        self.effect2 = effects.icon("unstable", 12, image_unstable)
        owner.effects.append(self.effect1)
        owner.effects.append(self.effect2)
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, owner.orient)
        self.owner = owner
        self.ori_image = image
        self.core = owner.core
        self.core.spaces.add(self)

        self.life = 8
        self.party = owner.party
        self.damage_range = size
        self.damage = 50
        self.attacked = []

        x, y, orient = self.absolute_location()
        self.image = pg.transform.rotate(self.ori_image, orient-90)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.life <= 0:
            self.life = 8
            self.attacked = []
            self.effect1.life = -1
            self.effect2.life += 8
        self.life -= 1
        if self.life % 2 == 0:
            self.orient += 90
            if self.orient > 360:
                self.orient -= 360
        self.loc_x = self.owner.loc_x
        self.loc_y = self.owner.loc_y
        x, y, orient = self.absolute_location()
        self.image = pg.transform.rotate(self.ori_image, orient-90)
        self.rect = self.image.get_rect(center=(x, y))

        angles = (60, 300)
        for entity in self.core.entities:
                if entity.party != self.party and entity not in self.attacked:
                    ori1 = math.degrees(math.atan2(entity.loc_y-self.loc_y, entity.loc_x-self.loc_x))
                    if (ori1 - self.orient)%360 < angles[0] or (ori1 - self.orient)%360 > angles[1]:
                        if (entity.loc_x-self.loc_x)**2+(entity.loc_y-self.loc_y)**2 < (self.damage_range+entity.size)**2:
                            entity.demage(self.damage)
                            self.attacked.append(entity)
        
        super().update()

    def remove(self):
        self.core.spaces.remove(self)
        self.effect1.life = 4

class healing(effects.icon):
    def __init__(self, owner, image, value, time, consumption):
        super().__init__('healing', time, image)
        self.owner = owner
        self.value = value
        self.consumption = consumption
        if magis_requirement(owner, consumption):
            for effect in owner.effects:
                if effect.eid == 'healing':
                    effect.life += time
                    return
            owner.effects.append(self)

    def update(self):
        self.owner.health_point += self.value
        if self.owner.health_point > self.owner.max_hp:
            self.owner.health_point = self.owner.max_hp
        super().update()

class heal():
    def __init__(self, owner, value, consumption):
        self.owner = owner
        self.value = value
        self.consumption = consumption
        if magis_requirement(owner, consumption):
            owner.health_point += value
            if owner.health_point > owner.max_hp:
                owner.health_point = owner.max_hp