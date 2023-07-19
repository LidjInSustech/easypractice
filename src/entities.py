import pygame as pg
import math
import util

margin = 4

class Visible(pg.sprite.Sprite):
    def __init__(self, camera, x, y, orient):
        super().__init__()
        self.camera = camera
        self.loc_x = x
        self.loc_y = y
        self.orient = orient
        #self.center = pg.display.get_surface().get_rect().center
        self.center = self.camera.center

    def absolute_location(self):
        if self.camera is None:
            raise Exception('Camera is not set')
        camera = self.camera
        rad = math.radians(camera.orient)
        cos = math.cos(rad)
        sin = math.sin(rad)
        dx = self.loc_x - camera.loc_x
        dy = self.loc_y - camera.loc_y
        ref_x = cos*dx + sin*dy
        ref_y = sin*dx - cos*dy
        return self.center[0]+ref_x, self.center[1]+ref_y, self.orient - self.camera.orient

class Entity(Visible):
    def __init__(self, core, x=0, y=0, orient=0, picture=None):
        super().__init__(core.camera, x, y, orient)
        if picture is None:
            #picture = pg.transform.scale(pg.image.load('./res/entity.png'),(48,48)).convert_alpha()
            picture = pg.Surface((64, 64), flags=pg.SRCALPHA)
            #picture = pg.Surface((64, 64))
            pg.draw.circle(picture, (12, 33, 120, 150), (32, 32), 32 - margin)
            pg.draw.polygon(picture, (250, 25, 55, 200), [(32, margin), (margin*2, 32), (64 - margin*2, 32)])
        #picture = pg.transform.rotate(picture, -90)
        self.ori_image = picture
        self.image = self.ori_image
        self.rect = self.image.get_rect()

        self.rect.center = self.center
        self.core = core

        self.size = 24

        self.max_hp = 1000
        self.health_point = self.max_hp
        self.max_mp = 1000
        self.magis_point = self.max_mp
        self.mp_recovery = 3
        self.speed = 5
        self.party = 0
        self.effects = []

    def update(self):
        super().update()

        self.magis_point += self.mp_recovery
        if self.health_point > self.max_hp:
            self.health_point = self.max_hp
        if self.magis_point > self.max_mp:
            self.magis_point = self.max_mp
        if self.health_point <= 0:
            self.core.entities.remove(self)
        
        i = 0
        while i < len(self.effects):
            self.effects[i].update()
            if self.effects[i].life == 0:
                del self.effects[i]
            else:
                i += 1

        x, y, orient = self.absolute_location()
        self.rect.center = (x, y)

        self.image = self.ori_image.copy()
        
        arc_rect = self.image.get_rect()
        pg.draw.arc(self.image, (155,155,155,200), arc_rect,
            math.pi*(2*self.health_point/self.max_hp+0.5), math.pi/2, width=margin)
        pg.draw.arc(self.image, (255,0,0,200), arc_rect,
            math.pi/2, math.pi*(2*self.health_point/self.max_hp+0.5), width=margin)

        self.image = pg.transform.rotate(self.image, orient-90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def demage(self, value):
        if any(effect.eid == 'invincible' for effect in self.effects):
            return
        self.health_point -= value
        self.core.spaces.add(demage_marker(self.core, self.loc_x, self.loc_y, self.orient, value))


class Prepared_entity(Entity):
    def __init__(self, core, skills, x=0, y=0, orient=0, picture=None):
        super().__init__(core, x, y, orient, picture)
        self.skills = skills

class demage_marker(Visible):
    def __init__(self, core, x, y, orient, value):
        super().__init__(core.camera, x, y, orient)
        self.core = core
        self.image = util.get_font(24).render(str(-value), True, (255, 0, 0), (0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        x, y, orient = self.absolute_location()
        self.rect.center = (x+20, y-20)
        self.life = 5

    def update(self):
        super().update()
        if self.life > 0:
            self.life -= 1
        else:
            self.core.spaces.remove(self)