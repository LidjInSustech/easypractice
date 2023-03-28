import pygame as pg
import entity
import cevent
import math

def generate(ref, owner):
    return Attack(ref, owner)

class Attack(entity.Entity):
    def __init__(self, ref, owner):
        super().__init__(ref)
        self.ori_image = pg.Surface((64, 64))
        self.ori_image.fill((255,255,255))
        self.ori_image.set_colorkey((255,255,255))
        pg.draw.polygon(self.ori_image, (0,255,255), [(0,64),(32,0),(64,64)])
        self.image = self.ori_image
        self.rect = self.image.get_rect()

        self.center = pg.display.get_surface().get_rect().center
        self.rect.center = self.center

        self.orient = ref.orient
        rad = math.radians(self.orient)
        self.loc_x = ref.loc_x - 64*math.sin(rad)
        self.loc_y = ref.loc_y - 64*math.cos(rad)

        self.show_orient = False

        self.owner = owner
        self.phase = 10
        pg.event.post(pg.event.Event(cevent.LIFE_BORN,{'sprite':self}))

    def update(self):
        super().update()
        ref_orient = self.orient - self.ref.orient
        self.image = pg.transform.rotate(self.ori_image, ref_orient)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.phase -= 1
        if self.phase == 0:
            pg.event.post(pg.event.Event(cevent.LIFE_KILL,{'sprite':self}))
            for entity in self.groups()[0]:
                if (entity.health_point is not None):
                    between = (self.loc_x-entity.loc_x, self.loc_y-entity.loc_y)
                    if between[0]**2+between[1]**2 < 32**2:
                        rad = math.radians(self.orient)
                        high = abs(between[0]*math.cos(rad)+between[1]*math.sin(rad))
                        if high < 16:
                            pg.event.post(pg.event.Event(
                                cevent.ATTACK,{'target':entity, 'damage':10}
                            ))
