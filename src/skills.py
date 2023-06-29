import pygame as pg
import math
import entities

class sample_cut(entities.Visible):
    def __init__(self, core, owner):
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, owner.orient)
        self.range = 100
        self.owner = owner
        picture = pg.Surface((self.range*2, self.range*2), flags=pg.SRCALPHA)
        pg.draw.arc(picture, (55,255,55,180), pg.Rect(0, 0, self.range*2, self.range*2), -math.pi/3, math.pi/3, width=int(self.range/2))
        self.ori_image = picture
        self.image = self.ori_image
        x, y, orient = self.absolute_location()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image = pg.transform.rotate(self.image, orient)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.life = 2
        self.core = core
        core.spaces.add(self)

    def update(self):
        super().update()

        if self.life > 0:
            self.life -= 1
        else:
            self.core.spaces.remove(self)
            for entity in self.core.entities:
                if entity != self.owner:
                    ori1 = math.degrees(math.atan2(entity.loc_y-self.loc_y, entity.loc_x-self.loc_x))
                    if (ori1 - self.orient)%360 < 60 or (ori1 - self.orient)%360 > 300:
                        if (entity.loc_x-self.loc_x)**2+(entity.loc_y-self.loc_y)**2 < (self.range+entity.size)**2:
                            entity.health_point -= 20
