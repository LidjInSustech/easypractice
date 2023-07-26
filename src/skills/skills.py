import pygame as pg
import math
import util
import visibles
import skills.entities as entities
import skills.fields as fields
import effects

class Skill():
    def __init__(self, owner, properties = None, accept_keys = None):
        self.owner = owner
        if properties is None:
            properties = owner.properties
        self.update_properties(properties)
        self.accept_keys = accept_keys

    def update_properties(self, properties):
        return

    def conduct(self, direction):
        return

    def get_direction(self, key_pressed, key_map):
        if self.accept_keys is None:
            return 'none'
        for key in reversed(key_pressed):
            for key_name in self.accept_keys:
                if key == key_map[key_name]:
                    return key_name
        return 'none'

    def consume_mp(self):
        if self.properties.get('mp_consumption', 0) > self.owner.mp:
            return False
        self.owner.mp -= self.properties.get('mp_consumption', 0)
        return True

class FastMove(Skill):
    def __init__(self, owner, properties = None):
        self.image = util.load_image_alpha('skills/fastmove.png')
        self.icon = util.load_image('effects/unstable.png')
        accept_keys = ['up', 'down', 'left', 'right', 'turn left', 'turn right']
        super().__init__(owner, properties, accept_keys)
        
    def update_properties(self, properties):
        origin = {'speed': 20, 'cd': 12, 'benefit_time': 4}
        origin['speed'] = properties.get('speed', 5)*origin['speed']
        origin['cd'] = properties.get('x_cd', 1)*origin['cd']
        origin['benefit_time'] = properties.get('x_benefit_time', 1)*origin['benefit_time']
        self.properties = origin
        image_size = origin['speed']*2
        self.image = pg.transform.scale(self.image, (image_size, image_size))

    def conduct(self, direction):
        orientation = None
        match direction:
            case 'up':
                orientation = 0
            case 'down':
                orientation = 180
            case 'left':
                orientation = 90
            case 'right':
                orientation = -90
            case 'turn left':
                self.owner.orientation += 75
            case 'turn right':
                self.owner.orientation -= 75
        if orientation is None:
            return
        if any([e.name == 'unstable' for e in self.owner.effects]):
            return
        self.owner.effects.append(effects.icon_countdown_effect('unstable', self.icon, self.properties['cd']))
        orientation += self.owner.orientation
        self.owner.loc += pg.math.Vector2(1, 0).rotate(orientation)*self.properties['speed']
        self.owner.controller.fields.add(fields.FastMove(self.owner, orientation, image = self.image))
        for e in self.owner.effects:
            if e.name == 'invincible':
                e.time += self.properties['benefit_time']
                return
        self.owner.effects.append(effects.countdown_effect('invincible', self.properties['benefit_time']))

class MagicBullet(Skill):
    def __init__(self, owner, properties = None):
        self.images = []
        self.images.append(util.load_image_alpha('skills/mag_sperm.png'))
        self.images.append(util.load_image_alpha('skills/mag_sperm1.png'))
        self.images.append(util.load_image_alpha('skills/mag_sperm2.png'))
        field_image = pg.Surface((32, 32))
        pg.draw.circle(field_image, (255,0,0), (16, 16), 16)
        field_image.set_colorkey((0,0,0))
        field_image.set_alpha(80)
        self.field_image = field_image
        super().__init__(owner, properties)

    def update_properties(self, properties):
        origin = {'max_hp': 100, 'max_mp': 0, 'mp_regen': 0, 'speed': 5, 'size': 8,
         'life': 100, 'attack': 60, 'cd': 6, 'extension': 1.1, 'mp_consumption': 100}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*4
        self.images = [pg.transform.scale(image, (image_size, image_size)) for image in self.images]
        image_size = self.properties['size']*2*origin['extension']
        self.field_image = pg.transform.scale(self.field_image, (image_size, image_size))

    def conduct(self, direction):
        if any([effects.name == 'spell_cd' for effects in self.owner.effects]):
            return
        self.owner.effects.append(effects.countdown_effect('spell_cd', self.properties['cd']))
        if not self.consume_mp():
            return
        orientation = self.owner.orientation
        entity = entities.MagicBullet(self.owner, self.images, self.owner.loc.copy(), orientation, self.properties)
        self.owner.controller.entities.add(entity)
        field = fields.MagicBullet(entity, self.field_image, self.properties)
        self.owner.controller.fields.add(field)
        
class HeavyCut(Skill):
    def __init__(self, owner, properties = None):
        size = 256
        image_f0 = pg.Surface((size, size), flags=pg.SRCALPHA)
        pg.draw.arc(image_f0, (255,0,0,80), pg.Rect(0, 0, size, size), math.pi/6, math.pi/6*5, width=int(size/2))
        image_f1 = util.load_image_alpha('skills/cut_f1.png')
        image_f2 = util.load_image_alpha('skills/cut_f2.png')
        self.f_images = [image_f0, image_f1, image_f2]
        image_r0 = pg.Surface((size, size), flags=pg.SRCALPHA)
        pg.draw.arc(image_r0, (255,0,0,80), pg.Rect(0, 0, size, size), 0, math.pi, width=int(size/2))
        image_r1 = util.load_image_alpha('skills/cut_t1.png')
        image_r2 = util.load_image_alpha('skills/cut_t2.png')
        self.r_images = [image_r0, image_r1, image_r2]

        accept_keys = ['up', 'left', 'right', 'turn left', 'turn right']
        super().__init__(owner, properties, accept_keys)

    def update_properties(self, properties):
        origin = {'size': 128, 'attack': 120, 'cd': 6, 'extension': 1, 'harmful_time': 10, 'base_cd': 12}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        self.f_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.f_images]
        self.r_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.r_images]
        self.l_images = [self.r_images[0], pg.transform.flip(self.r_images[1], True, False), pg.transform.flip(self.r_images[2], True, False)]

    def conduct(self, direction):
        if any([effects.name == 'unstable' for effects in self.owner.effects]):
            return
        if any([effects.name == 'sword_cd' for effects in self.owner.effects]):
            return
        self.owner.effects.append(effects.countdown_effect('sword_cd', self.properties['base_cd'] + self.properties['cd']))
        self.owner.effects.append(effects.countdown_effect('unstable', self.properties['base_cd'] + self.properties['harmful_time']))
        self.owner.effects.append(effects.countdown_effect('unmovable', self.properties['base_cd']))
        orientation = self.owner.orientation
        match direction:
            case 'up':
                e = fields.Cut(self.owner, self.owner.loc.copy(), orientation, self.f_images, self.properties)
            case 'left':
                orientation += 90
                e = fields.Cut(self.owner, self.owner.loc.copy(), orientation, self.f_images, self.properties)
            case 'right':
                orientation -= 90
                e = fields.Cut(self.owner, self.owner.loc.copy(), orientation, self.f_images, self.properties)
            case 'turn left':
                orientation += 90
                e = fields.Cut(self.owner, self.owner.loc.copy(), orientation, self.l_images, self.properties, side = True)
            case 'turn right':
                orientation -= 90
                e = fields.Cut(self.owner, self.owner.loc.copy(), orientation, self.r_images, self.properties, side = True)
            case _:
                e = fields.Cut(self.owner, self.owner.loc.copy(), orientation, self.f_images, self.properties)
        self.owner.controller.fields.add(e)

class FastCut(HeavyCut):
    def update_properties(self, properties):
        origin = {'size': 96, 'attack': 60, 'cd': 4, 'extension': 1, 'harmful_time': 4, 'base_cd': 7}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        self.f_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.f_images]
        self.r_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.r_images]
        self.l_images = [self.r_images[0], pg.transform.flip(self.r_images[1], True, False), pg.transform.flip(self.r_images[2], True, False)]
