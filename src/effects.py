import pygame as pg
import math

class effect():
    def __init__(self, life):
        self.life = life
    def update(self):
        if self.life > 0:
            self.life -= 1

class base_move(effect):
    def __init__(self):
        super().__init__(1)

    def movable(self):
        for effect in self.owner.effects:
            if isinstance(effect, unmovable):
                return False
        return True
    
    def update(self):
        pass

class simple_forward(base_move):
    def __init__(self, owner, speed):
        super().__init__()
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
        super().__init__()
        self.owner = owner
        self.speed = speed
    def update(self):
        self.life = 0
        if not self.movable():
            return
        self.owner.orient += self.speed

class icon(effect):
    def __init__(self, life):
        super().__init__(life)
        self.image = pg.font.SysFont('Calibri', 32).render('E', False, (255, 255, 255), (0, 0, 0))

class unmovable(icon):
    def __init__(self, life):
        super().__init__(life)

class unstable(icon):
    def __init__(self, life):
        super().__init__(life)
