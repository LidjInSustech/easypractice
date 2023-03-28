import pygame as pg
import math
import cevent

class Entity(pg.sprite.Sprite):
    def __init__(self, ref = None):
        super().__init__()
        picture = pg.transform.scale(pg.image.load('./res/entity.png'),(48,48)).convert()
        self.ori_image = pg.Surface((64, 64))
        self.ori_image.fill((255,255,255))
        self.ori_image.blit(picture, (8, 8))
        self.ori_image.set_colorkey((255,255,255))
        self.image = self.ori_image
        self.rect = self.image.get_rect()

        self.center = pg.display.get_surface().get_rect().center
        self.rect.center = self.center
        self.ref = ref

        self.loc_x = 0
        self.loc_y = 0
        self.orient = 0

        self.health_point = None
        self.max_hp = None
        self.magis_point = None
        self.max_mp = None
        self.show_orient = True


    def update(self):
        super().update()
        if self.ref is not None:
            ref = self.ref
            rad = math.radians(ref.orient)
            cos = math.cos(rad)
            sin = math.sin(rad)
            dx = self.loc_x - ref.loc_x
            dy = self.loc_y - ref.loc_y
            ref_x = cos*dx - sin*dy
            ref_y = sin*dx + cos*dy
            self.rect.center = (self.center[0]+ref_x, self.center[1]+ref_y)
        
        self.image = self.ori_image.copy()
        if (self.max_hp is not None) & (self.health_point is not None):
            pg.draw.arc(self.image, (255,0,0), pg.Rect(8,8,48,48),
                 math.pi/2, math.pi*(2*self.health_point/100+0.5), width=6)
        
        if self.show_orient:
            rad = 0
            if self.ref is not None:
                rad = math.radians(self.orient - self.ref.orient)
            points = [(32-l*math.sin(rad+r),32-l*math.cos(rad+r)) 
                for l,r in [(25, math.pi/9),(32, 0),(25, -math.pi/9)]]
            pg.draw.polygon(self.image, (0,0,255), points)

    def damage(self, value):
        if self.health_point is not None:
            self.health_point -= value
            if self.health_point < 0:
                pg.event.post(pg.event.Event(cevent.LIFE_KILL, {'sprite':self}))