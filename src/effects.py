import pygame as pg
import math

class effect():
    def __init__(self, eid, life):
        self.eid = eid
        self.life = life
    def update(self):
        if self.life > 0:
            self.life -= 1

class base_move(effect):
    def __init__(self, eid="base_move"):
        super().__init__(eid, 1)

    def movable(self):
        for effect in self.owner.effects:
            if effect.eid == "unmovable":
                return False
        return True
    
    def update(self):
        pass

class simple_forward(base_move):
    def __init__(self, owner, speed):
        super().__init__("simple_forward")
        self.owner = owner
        self.speed = speed
    def update(self):
        self.life = 0
        if not self.movable():
            return
        self.owner.loc_x += self.speed * math.cos(math.radians(self.owner.orient))
        self.owner.loc_y += self.speed * math.sin(math.radians(self.owner.orient))

class simple_turn(base_move):
    def __init__(self, owner, speed):
        super().__init__("simple_turn")
        self.owner = owner
        self.speed = speed
    def update(self):
        self.life = 0
        if not self.movable():
            return
        self.owner.orient += self.speed

class simple_slide(base_move):
    '''positive speed for right'''
    def __init__(self, owner, speed):
        super().__init__("simple_slide")
        self.owner = owner
        self.speed = speed
    def update(self):
        self.life = 0
        if not self.movable():
            return
        self.owner.loc_x += self.speed * math.sin(math.radians(self.owner.orient))
        self.owner.loc_y -= self.speed * math.cos(math.radians(self.owner.orient))

class icon(effect):
    def __init__(self, eid, life, picture):
        super().__init__(eid, life)
        if picture is None:
            self.image = pg.Surface((32,32))
            self.image.fill((0,0,0))
            pg.draw.circle(self.image, (255,255,255), (16,16), 13)
        else:
            self.image = picture
