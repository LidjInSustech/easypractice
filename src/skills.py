import pygame as pg
import math
import entities
import effects
import sub_skill
import util

class basic():
    def __init__(self, directions = None, finaldir = 'C'):
        self.directions = directions
        self.finaldir = finaldir
        self.reflist = {'F':'up', 'B':'down', 'L':'left', 'R':'right', 'LT':'turn left', 'RT':'turn right'}

    def act(self, owner, direction):
        #direction in F(forth), B(back), L(left), R(right), C(center), LT(turn left), RT(turn ritht)
        return

    def act_withkeys(self, owner, keys, ref):
        if self.directions == None:
            return self.act(owner, self.finaldir)
        i = len(keys) - 1
        while i >= 0:
            key = keys[i]
            for direction in self.directions:
                if key == ref[self.reflist[direction]]:
                    return self.act(owner, direction)
            i -= 1
        return self.act(owner, self.finaldir)

class fast_move(basic):
    def __init__(self):
        super().__init__(['F', 'B', 'L', 'R', 'LT', 'RT'], 'C')
        picture = pg.Surface((16,16))
        picture.fill((255,255,255))
        picture.set_colorkey((255,255,255))
        pg.draw.line(picture, (0,0,0),(8,8),(0,8),3)
        self.picture = picture
        self.image_unstable = util.load_image('effects/unstable.png')
        self.image_invincible = util.load_image('effects/invincible.png')

    def act(self, owner, direction):
        multiple = 20
        if direction == 'F':
            sub_skill.fast_forward(owner, owner.orient, self.picture, owner.speed*multiple, self.image_unstable, self.image_invincible)
        elif direction == 'B':
            sub_skill.fast_forward(owner, owner.orient+180, self.picture, owner.speed*multiple, self.image_unstable, self.image_invincible)
        elif direction == 'L':
            sub_skill.fast_forward(owner, owner.orient+90, self.picture, owner.speed*multiple, self.image_unstable, self.image_invincible)
        elif direction == 'R':
            sub_skill.fast_forward(owner, owner.orient-90, self.picture, owner.speed*multiple, self.image_unstable, self.image_invincible)
        elif direction == 'LT':
            sub_skill.fast_turn(owner, 80)
        elif direction == 'RT':
            sub_skill.fast_turn(owner, -80)

    def act_withkey(self, owner, key, ref):
        if key == ref['up']:
            self.act(owner, 'F')
        elif key == ref['down']:
            self.act(owner, 'B')
        elif key == ref['left']:
            self.act(owner, 'L')
        elif key == ref['right']:
            self.act(owner, 'R')
        elif key == ref['turn left']:
            self.act(owner, 'LT')
        elif key == ref['turn right']:
            self.act(owner, 'RT')
        else:
            return

class magic_sperm(basic):
    def __init__(self):
        super().__init__()
        size = 32
        self.i0 = util.load_image_alpha('skills/mag_sperm.png', size, size)
        self.i1 = util.load_image_alpha('skills/mag_sperm1.png', size, size)
        self.i2 = util.load_image_alpha('skills/mag_sperm2.png', size, size)

    def act(self, owner, direction):
        sub_skill.magic_sperm(owner, owner.orient, [self.i0, self.i1, self.i2])

class slow_cut(basic):
    def __init__(self):
        super().__init__(['F', 'L', 'R', 'LT', 'RT'], 'C')
        size = 200
        self.i0 = pg.Surface((size, size), flags=pg.SRCALPHA)
        pg.draw.arc(self.i0, (255,0,0,80), pg.Rect(0, 0, size, size), math.pi/6, math.pi/6*5, width=int(size/3))
        self.i1 = util.load_image_alpha('skills/cut_f1.png', size, size)
        self.i2 = util.load_image_alpha('skills/cut_f2.png', size, size)
        self.it = pg.Surface((size, size), flags=pg.SRCALPHA)
        pg.draw.arc(self.it, (255,0,0,80), pg.Rect(0, 0, size, size), 0, math.pi, width=int(size/3))
        self.ir1 = util.load_image_alpha('skills/cut_t1.png', size, size)
        self.ir2 = util.load_image_alpha('skills/cut_t2.png', size, size)
        self.il1 = pg.transform.flip(self.ir1, True, False)
        self.il2 = pg.transform.flip(self.ir2, True, False)
        self.unmovable_image = util.load_image('effects/unmovable.png')
        self.size = size
        self.slow = True

    def act(self, owner, direction):
        if direction == 'L':
            sub_skill.slow_cut(owner, owner.orient+90, [self.i0, self.i1, self.i2], self.unmovable_image, self.size, slow = self.slow)
        elif direction == 'R':
            sub_skill.slow_cut(owner, owner.orient-90, [self.i0, self.i1, self.i2], self.unmovable_image, self.size, slow = self.slow)
        elif direction == 'LT':
            sub_skill.slow_cut(owner, owner.orient+90, [self.it, self.il1, self.il2], self.unmovable_image, self.size, slow = self.slow, side = True)
        elif direction == 'RT':
            sub_skill.slow_cut(owner, owner.orient-90, [self.it, self.ir1, self.ir2], self.unmovable_image, self.size, slow = self.slow, side = True)
        else:
            sub_skill.slow_cut(owner, owner.orient, [self.i0, self.i1, self.i2], self.unmovable_image, self.size, slow = self.slow)

class fast_cut(slow_cut):
    def __init__(self):
        super().__init__()
        self.slow = False

class missile(basic):
    def __init__(self):
        super().__init__()
        size = 48
        self.i0 = util.load_image_alpha('skills/missile1.png', size, size)
        self.i1 = util.load_image_alpha('skills/missile2.png', size, size)
        self.i2 = util.load_image_alpha('skills/missile3.png', size, size)

    def act(self, owner, direction):
        sub_skill.missile(owner, owner.orient, [self.i0, self.i1, self.i2])

class fireball(basic):
    def __init__(self):
        super().__init__()
        size1 = 64
        size2 = 192
        self.i0 = util.load_image_alpha('skills/fireball1.png', size1, size1)
        self.i1 = util.load_image_alpha('skills/fireball2.png', size1, size1)
        self.i2 = util.load_image_alpha('skills/fireball3.png', size1, size1)
        self.i = util.load_image_alpha('skills/fireball_final.png', size2, size2)
        self.size1 = 24
        self.size2 = 80

    def act(self, owner, direction):
        sub_skill.fireball(owner, owner.orient, [self.i0, self.i1, self.i2], self.i, self.size1, self.size2)

class helix_cut(basic):
    def __init__(self):
        super().__init__()
        size = 200
        image = pg.Surface((size, size), flags=pg.SRCALPHA)
        pg.draw.arc(image, (255,0,0,80), pg.Rect(0, 0, size, size), math.pi/6, math.pi/6*5, width=int(size/3))
        image.blit(util.load_image_alpha('skills/cut_f2.png', size, size), (0,0))
        self.image = image
        self.image_unstable = util.load_image('effects/unstable.png')
        self.working = None
        self.size = size//2

    def act(self, owner, direction):
        if self.working == None:
            self.working = sub_skill.helix_cut(owner, self.image, self.size, self.image_unstable)
        else:
            self.working.remove()
            self.working = None

class healing(basic):
    def __init__(self):
        super().__init__()
        self.image = util.load_image_alpha('effects/healing.png', 32, 32)

    def act(self, owner, direction):
        sub_skill.healing(owner, self.image, 1, 100, 200)

class heal(basic):
    def act(self, owner, direction):
        sub_skill.heal(owner, 100, 400)