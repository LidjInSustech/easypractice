import pygame as pg
import math

class effect():
    def __init__(self, eid, life):
        self.eid = eid
        self.life = life
    def update(self):
        if self.life > 0:
            self.life -= 1
    def __str__(self):
        return f'{self.eid}: {self.life}'
    def __repr__(self):
        return self.__str__()

class base_move(effect):
    def __init__(self, eid="base_move"):
        super().__init__(eid, 1)
    
    def update(self):
        self.life = 0
        for effect in self.owner.effects:
            if effect.eid == "unmovable":
                return
        colisions = []
        o = self.owner
        ori_x = o.loc_x
        ori_y = o.loc_y
        for e in o.core.entities:
            if e.party != o.party:
                if (e.loc_x - o.loc_x)**2 + (e.loc_y - o.loc_y)**2 < (e.size + o.size)**2:
                    colisions.append(e)
        self.act()
        for e in o.core.entities:
            if e.party != o.party:
                if (e.loc_x - o.loc_x)**2 + (e.loc_y - o.loc_y)**2 < (e.size + o.size)**2:
                    if e not in colisions:
                        o.loc_x = ori_x
                        o.loc_y = ori_y
                        return
    
    def act(self):
        pass
        

class simple_forward(base_move):
    def __init__(self, owner, speed):
        super().__init__("simple_forward")
        self.owner = owner
        self.speed = speed
    def act(self):
        self.owner.loc_x += self.speed * math.cos(math.radians(self.owner.orient))
        self.owner.loc_y += self.speed * math.sin(math.radians(self.owner.orient))

class simple_turn(base_move):
    def __init__(self, owner, speed):
        super().__init__("simple_turn")
        self.owner = owner
        self.speed = speed
    def update(self):
        self.life = 0
        for effect in self.owner.effects:
            if effect.eid == "unmovable":
                return
        self.owner.orient += self.speed

class simple_slide(base_move):
    '''positive speed for right'''
    def __init__(self, owner, speed):
        super().__init__("simple_slide")
        self.owner = owner
        self.speed = speed
    def act(self):
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
