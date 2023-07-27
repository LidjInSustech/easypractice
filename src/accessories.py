import pygame as pg
import visibles
import math

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
        hp = self.owner.hp/max(self.owner.max_hp, 1)
        hp = max(0, min(1, hp))
        hp = pg.math.lerp(0, self.length, hp)
        self.origional_image.fill((255, 0, 0), (self.length - hp, 0, hp, self.height))
        mp = self.owner.mp/max(self.owner.max_mp, 1)
        mp = max(0, min(1, mp))
        mp = pg.math.lerp(0, self.length, mp)
        self.origional_image.fill((0, 0, 255), (self.length, 0, mp, self.height))
        super().update()

class State_ring(visibles.Accessory):
    def __init__(self, owner, width = 4):
        size = owner.radius + width
        image_source = pg.Surface((size*2, size*2), pg.SRCALPHA)
        pg.draw.circle(image_source, (100, 100, 100), (size, size), size, width)
        self.image_source = image_source
        self.width = width
        self.size = size
        super().__init__(owner, drift = None, image = image_source, rotate_image = False)

    def update(self):
        self.origional_image = self.image_source.copy()
        rect = self.origional_image.get_rect()
        hp = self.owner.hp/max(self.owner.max_hp, 1)
        hp = max(0, min(1, hp))
        hp = pg.math.lerp(0, math.pi, hp)
        pg.draw.arc(self.origional_image, (255, 0, 0), rect, math.pi*3/2 - hp, math.pi*3/2, self.width)
        mp = self.owner.mp/max(self.owner.max_mp, 1)
        mp = max(0, min(1, mp))
        mp = pg.math.lerp(0, math.pi, mp)
        pg.draw.arc(self.origional_image, (0, 0, 255), rect, math.pi*3/2, math.pi*3/2 + mp, self.width)
        super().update()