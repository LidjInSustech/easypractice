import pygame as pg
import math

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
    def __init__(self, core, camera):
        super().__init__(camera, 0, 0, 0)
        #picture = pg.transform.scale(pg.image.load('./res/entity.png'),(48,48)).convert_alpha()
        picture = pg.Surface((64, 64), flags=pg.SRCALPHA)
        #picture = pg.Surface((64, 64))
        pg.draw.circle(picture, (12, 33, 120, 150), (32, 32), 32 - margin)
        pg.draw.polygon(picture, (250, 25, 55, 200), [(32, margin), (margin*2, 32), (64 - margin*2, 32)])
        picture = pg.transform.rotate(picture, -90)
        self.ori_image = picture
        self.image = self.ori_image
        self.rect = self.image.get_rect()

        self.rect.center = self.center
        self.core = core

        self.size = 20

        self.health_point = 100
        self.max_hp = 100
        self.magis_point = 100
        self.max_mp = 100
        self.effects = []

    def update(self):
        super().update()
        
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
        
        pg.draw.arc(self.image, (155,155,155,200), pg.Rect(0,0,64,64),
            math.pi*(2*self.health_point/self.max_hp+0.5), math.pi/2, width=margin)
        pg.draw.arc(self.image, (255,0,0,200), pg.Rect(0,0,64,64),
            math.pi/2, math.pi*(2*self.health_point/self.max_hp+0.5), width=margin)

        self.image = pg.transform.rotate(self.image, orient)
        self.rect = self.image.get_rect(center=self.rect.center)