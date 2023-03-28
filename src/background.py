import pygame as pg
import entity

class Background(entity.Entity):
    def __init__(self, ref):
        super().__init__(ref)
        image = pg.image.load('./res/bigBackground.png')
        image = pg.transform.scale(image,(1024,1024)).convert()
        image.set_colorkey((255,255,255))
        self.ori_image = image
        self.image = image
        self.rect = self.image.get_rect()

        self.show_orient = False

    def update(self):
        super().update()
        ref_orient = self.orient - self.ref.orient
        self.image = pg.transform.rotate(self.ori_image, ref_orient)
        self.rect = self.image.get_rect(center=self.rect.center)