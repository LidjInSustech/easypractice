import pygame as pg
import visibles

class Direction_indicator(visibles.Accessory):
    def __init__(self, owner):
        image = pg.Surface((16, 8), pg.SRCALPHA)
        pg.draw.polygon(image, (25, 255, 25), ((16, 8), (8, 0), (0, 8)))
        drift = pg.math.Vector2(owner.radius + 4, 0)
        super().__init__(owner, drift = drift, image = image, rotate_image = True)

class State_bar(visibles.Accessory):
    def __init__(self, owner, length = None, height = 4):
        if length is None:
            length = owner.radius
        image = pg.Surface((length*2, height))
        image.fill((100, 100, 100))
        hp = pg.math.lerp(0, length, owner.hp/owner.max_hp)
        image.fill((255, 0, 0), (length - hp, 0, length, height))
        mp = pg.math.lerp(0, length, owner.mp/owner.max_mp)
        image.fill((0, 0, 255), (length, 0, length + mp, height))
        self.length = length
        self.height = height
        drift = pg.math.Vector2(0, owner.radius + 4)
        super().__init__(owner, drift = drift, image = image, rotate_image = False)

    def update(self):
        self.origional_image.fill((100, 100, 100))
        hp = self.owner.hp/self.owner.max_hp
        hp = max(0, min(1, hp))
        hp = pg.math.lerp(0, self.length, hp)
        self.origional_image.fill((255, 0, 0), (self.length - hp, 0, hp, self.height))
        mp = self.owner.mp/self.owner.max_mp
        mp = max(0, min(1, mp))
        mp = pg.math.lerp(0, self.length, mp)
        self.origional_image.fill((0, 0, 255), (self.length, 0, mp, self.height))
        super().update()