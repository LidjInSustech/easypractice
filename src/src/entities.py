import pygame as pg
import math

margin = 4

class Entity(pg.sprite.Sprite):
    def __init__(self, camera):
        super().__init__()
        #picture = pg.transform.scale(pg.image.load('./res/entity.png'),(48,48)).convert_alpha()
        picture = pg.Surface((64, 64))
        pg.draw.circle(picture, (12, 33, 120, 150), (32, 32), 32 - margin)
        pg.draw.polygon(picture, (250, 25, 55, 200), [(32, margin), (margin*2, 32), (64 - margin*2, 32)])
        self.ori_image = picture
        self.image = self.ori_image
        self.rect = self.image.get_rect()

        self.center = pg.display.get_surface().get_rect().center
        self.rect.center = self.center
        self.camera = camera

        self.loc_x = 0
        self.loc_y = 0
        self.orient = 0
        self.size = 20

        self.health_point = 100
        self.max_hp = 100
        self.magis_point = 100
        self.max_mp = 100
        self.effects = []

    def update(self):
        super().update()
        
        i = 0
        while i < len(self.effects):
            self.effects[i].update()
            if self.effects[i].life == 0:
                del self.effects[i]
            else:
                i += 1

        camera = self.camera
        rad = math.radians(camera.orient)
        cos = math.cos(rad)
        sin = math.sin(rad)
        dx = self.loc_x - camera.loc_x
        dy = self.loc_y - camera.loc_y
        ref_x = cos*dx - sin*dy
        ref_y = sin*dx + cos*dy
        self.rect.center = (self.center[0]+ref_x, self.center[1]+ref_y)

        self.image = self.ori_image.copy()
        ref_orient = self.orient - self.camera.orient
        self.image = pg.transform.rotate(self.ori_image, ref_orient)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        if (self.max_hp is not None) & (self.health_point is not None):
            pg.draw.arc(self.image, (255,0,0,200), pg.Rect(0,0,64,64),
                 math.pi/2, math.pi*(2*self.health_point/100+0.5), width=margin)