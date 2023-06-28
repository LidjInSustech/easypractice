import pygame as pg
import math
import core

class sample_cut(pg.sprite.Sprite):
    def __init__(self, core, owner, x, y, orient):
        super().__init__()
        self.owner = owner
        self.loc_x = x
        self.loc_y = y
        self.orient = orient
        picture = pg.Surface((80, 80))
        pg.draw.arc(picture, (55,255,55,100), pg.Rect(0,0,80,80), 0, math.pi, width=40)
        self.ori_image = picture
        self.image = self.ori_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.center = self.rect.center
        self.camera = owner.camera
        self.life = 2
        core.spaces.add(self)

    def update(self):
        super().update()

        if self.life > 0:
            self.life -= 1
        else:
            for entity in core.entities:
                if entity != owner:
                    ori1 = math.atan2(entity.loc_y-self.loc_y, entity.loc_x-self.loc_x)
                    if abs(ori1 - self.orient) < 45:
                        if (entity.loc_x-self.loc_x)**2+(entity.loc_y-self.loc_y)**2 < (40+entity.radius)**2:
                            #entity.hurt(20)
                            entity.health_point -= 20
