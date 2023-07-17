import pygame as pg
import math
import entities
import effects
import sub_skill
import util

class basic():
    def act(self, owner, direction):
        #direction in F(forth), B(back), L(left), R(right), C(center), LT(turn left), RT(turn ritht)
        return

    def act_withkeys(self, owner, keys, ref):
        #print(keys)
        return

class fast_move(basic):
    def __init__(self):
        picture = pg.Surface((16,16))
        picture.fill((255,255,255))
        picture.set_colorkey((255,255,255))
        pg.draw.line(picture, (0,0,0),(8,8),(0,8),3)
        self.picture = picture
        self.image_unstable = util.load_image('effects/unstable.png')
        self.image_escaping = util.load_image('effects/escaping.png')

    def act(self, owner, direction):
        multiple = 20
        if any([effect.eid in ("unstable", "unmovable") for effect in owner.effects]):
            return
        if direction == 'F':
            sub_skill.fast_forward(owner, self.picture, owner.speed*multiple, self.image_unstable, self.image_escaping)
        elif direction == 'B':
            sub_skill.fast_forward(owner, self.picture, -owner.speed*multiple, self.image_unstable, self.image_escaping)
        elif direction == 'L':
            sub_skill.fast_slide(owner, self.picture, -owner.speed*multiple, self.image_unstable, self.image_escaping)
        elif direction == 'R':
            sub_skill.fast_slide(owner, self.picture, owner.speed*multiple, self.image_unstable, self.image_escaping)
        elif direction == 'LT':
            sub_skill.fast_turn(owner, 80)
        elif direction == 'RT':
            sub_skill.fast_turn(owner, -80)

    def act_withkeys(self, owner, keys, ref):
        i = len(keys) - 1
        while i >= 0:
            if keys[i] == ref['up']:
                self.act(owner, 'F')
                break
            elif keys[i] == ref['down']:
                self.act(owner, 'B')
                break
            elif keys[i] == ref['left']:
                self.act(owner, 'L')
                break
            elif keys[i] == ref['right']:
                self.act(owner, 'R')
                break
            elif keys[i] == ref['turn left']:
                self.act(owner, 'LT')
                break
            elif keys[i] == ref['turn right']:
                self.act(owner, 'RT')
                break
            i -= 1

    def act_withkey(self, owner, key, ref):
        if key == ref['up']:
            self.act(owner, 'F')
        if key == ref['down']:
            self.act(owner, 'B')
        if key == ref['left']:
            self.act(owner, 'L')
        if key == ref['right']:
            self.act(owner, 'R')
        if key == ref['turn left']:
            self.act(owner, 'LT')
        if key == ref['turn right']:
            self.act(owner, 'RT')


class sample_cut(entities.Visible):
    def __init__(self, owner):
        super().__init__(owner.camera, owner.loc_x, owner.loc_y, owner.orient)
        self.range = 100
        self.owner = owner
        picture = pg.Surface((self.range*2, self.range*2), flags=pg.SRCALPHA)
        pg.draw.arc(picture, (0,0,0,100), pg.Rect(0, 0, self.range*2, self.range*2), -math.pi/3, math.pi/3, width=int(self.range/2))
        self.ori_image = picture
        self.image = self.ori_image
        x, y, orient = self.absolute_location()
        self.image = pg.transform.rotate(self.image, orient)
        self.rect = self.image.get_rect(center=(x, y))
        self.life = 2
        self.core = owner.core
        self.core.spaces.add(self)

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

class fire_boll(entities.Entity):
    def __init__(self, owner):
        image_size = 32
        picture = pg.Surface((2*image_size, 2*image_size), flags=pg.SRCALPHA)
        pg.draw.circle(picture, (255, 0, 0, 200), (image_size, image_size), image_size)
        pg.draw.circle(picture, (255, 255, 0, 200), (image_size, image_size), image_size//2)
        x_forward = math.cos(math.radians(owner.orient))*image_size*2 + owner.loc_x
        y_forward = math.sin(math.radians(owner.orient))*image_size*2 + owner.loc_y
        super().__init__(owner.core, x_forward, y_forward, owner.orient, picture)
        self.end_image = pg.Surface((2*image_size, 2*image_size), flags=pg.SRCALPHA)
        pg.draw.circle(self.end_image, (0,0,0,100), (image_size, image_size), image_size)
        self.core = owner.core
        self.owner = owner
        self.speed = 10
        self.range = image_size
        self.life = 60
        self.size = image_size
        self.health_point = 10
        self.max_hp = 10

        consume = 10
        if owner.magis_point > consume:
            owner.magis_point -= consume
            self.core.entities.add(self)
            
            owner.effects.append(effects.unmovable(10))

    def update(self):
        self.effects.append(effects.simple_forward(self, self.speed))
        super().update()
        if self.life <= 0:
            self.core.entities.remove(self)
        else:
            self.life -= 1
            for entity in self.core.entities:
                if entity == self.owner:
                    continue
                elif entity == self:
                    continue
                elif (entity.loc_x-self.loc_x)**2+(entity.loc_y-self.loc_y)**2 < (self.range+entity.size)**2:
                    entity.health_point -= 40
                    self.image = self.end_image
                    self.life = 0
