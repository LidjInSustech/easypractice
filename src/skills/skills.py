import pygame as pg
import math
import util
import visibles
import skills.entities as entities
import skills.fields as fields
import skills.effects as E
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

    def stop(self):
        return

    def get_direction(self, key_pressed, key_map):
        if self.accept_keys is None:
            return 'none'
        for key in reversed(key_pressed):
            for key_name in self.accept_keys:
                if key == key_map[key_name]:
                    return key_name
        return 'none'

    def consume_mp(self, value = None):
        if value is None:
            value = self.properties.get('mp_consumption', 0)
        if value > self.owner.mp:
            return False
        self.owner.mp -= value
        return True

class FastMove(Skill):
    def __init__(self, owner, properties = None):
        self.image = util.load_image_alpha('skills/fastmove.png')
        self.icon = util.load_image('effects/unstable.png')
        accept_keys = ['up', 'down', 'left', 'right', 'turn left', 'turn right']
        super().__init__(owner, properties, accept_keys)
        
    def update_properties(self, properties):
        origin = {'x_speed': 20, 'cd': 12, 'benefit_time': 4}
        origin['speed'] = properties.get('speed', 5)*origin['x_speed']
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
        if any([e.name == 'busy' for e in self.owner.effects]):
            return
        orientation += self.owner.orientation
        self.owner.loc += pg.math.Vector2(1, 0).rotate(orientation)*self.properties['speed']
        self.owner.controller.fields.add(fields.FastMove(self.owner, orientation, image = self.image))
        self.owner.effect_extend(effects.countdown_effect('invincible', self.properties['benefit_time']))
        
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
        accept_keys = ['up', 'left', 'right', 'down']
        super().__init__(owner, properties, accept_keys = accept_keys)

    def update_properties(self, properties):
        origin = {'max_hp': 100, 'max_mp': 1, 'mp_regen': 0, 'speed': 5, 'size': 8, 'knockback': 8,
         'life': 1000, 'attack': 60, 'extension': 1.1, 'mp_consumption': 50, 'before': 8, 'duration': 8, 'after': 12}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*4
        self.images = [pg.transform.scale(image, (image_size, image_size)) for image in self.images]
        image_size = self.properties['size']*2*origin['extension']
        self.field_image = pg.transform.scale(self.field_image, (image_size, image_size))

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if direction in ('up', 'down'):
            if self.consume_mp(self.properties['mp_consumption']*3):
                # begin to cast
                if direction == 'up':
                    self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
                    for i in [-30, 0, 30]:
                        orientation = i + self.owner.orientation
                        self.post(orientation)
                    return
                else:
                    self.owner.effects.append(effects.countdown_effect('busy',
                     self.properties['before'] + self.properties['duration'] + self.properties['after']))
                    self.owner.effect_extend(effects.countdown_effect('unmovable',
                     self.properties['before'] + self.properties['duration']))
                    for i in range(3):
                        time = self.properties['before'] + self.properties['duration']*i/2
                        self.owner.effects.append(effects.delay_action(time, lambda :self.post(self.owner.orientation)))
        elif self.consume_mp():
            # begin to cast
            match direction:
                case 'left':
                    orientation = 90
                case 'right':
                    orientation = -90
                case _:
                    orientation = 0
            self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
            orientation += self.owner.orientation
            self.post(orientation)
    
    def post(self, orientation):
        entity = entities.MagicBullet(self.owner, self.images, self.owner.loc.copy(), orientation, self.properties)
        self.owner.controller.entities.add(entity)
        entity.handle_image()
        field = fields.MagicBullet(entity, self.field_image, self.properties)
        self.owner.controller.fields.add(field)
        field.handle_image()
        
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
        origin = {'size': 128, 'attack': 120, 'extension': 1, 'before': 11, 'duration': 5, 'after': 4}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        self.f_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.f_images]
        self.r_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.r_images]
        self.l_images = [self.r_images[0], pg.transform.flip(self.r_images[1], True, False), pg.transform.flip(self.r_images[2], True, False)]

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        self.owner.effects.append(effects.countdown_effect('busy', self.properties['before']+self.properties['duration'] + self.properties['after']))
        self.owner.effect_extend(effects.countdown_effect('unmovable', self.properties['before']+self.properties['duration']))
        match direction:
            case 'up':
                e = fields.Cut(self.owner, 0, self.f_images, self.properties)
            case 'left':
                e = fields.Cut(self.owner, 90, self.f_images, self.properties)
            case 'right':
                e = fields.Cut(self.owner, -90, self.f_images, self.properties)
            case 'turn left':
                e = fields.Cut(self.owner, 90, self.l_images, self.properties, side = True)
            case 'turn right':
                e = fields.Cut(self.owner, -90, self.r_images, self.properties, side = True)
            case _:
                e = fields.Cut(self.owner, 0, self.f_images, self.properties)
        self.owner.controller.fields.add(e)

class FastCut(HeavyCut):
    def update_properties(self, properties):
        origin = {'size': 96, 'attack': 60, 'extension': 1, 'before': 1, 'duration': 5, 'after': 6}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        self.f_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.f_images]
        self.r_images = [pg.transform.scale(image, (image_size, image_size)) for image in self.r_images]
        self.l_images = [self.r_images[0], pg.transform.flip(self.r_images[1], True, False), pg.transform.flip(self.r_images[2], True, False)]

class HeavyLunge(Skill):
    def __init__(self, owner, properties = None):
        self.image1 = util.load_image_alpha('skills/lunge1.png')
        self.image2 = util.load_image_alpha('skills/lunge2.png')

        accept_keys = ['up', 'left', 'right', 'turn left', 'turn right']
        super().__init__(owner, properties, accept_keys)

    def update_properties(self, properties):
        origin = {'length': 64, 'width':32, 'attack': 120, 'extension': 1, 'before': 11, 'duration': 5, 'after': 4, 'dash': 64}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        origin['length'] = properties.get('x_size', 1)*origin['length']
        origin['width'] = properties.get('x_size', 1)*origin['width']
        self.properties = origin
        length = self.properties['length']
        width = self.properties['width']
        self.image1 = pg.transform.scale(self.image1, (2*width, 2*length))
        self.image2 = pg.transform.scale(self.image2, (2*width, 2*length))
        c_image = pg.Surface((2*width, 2*length), flags=pg.SRCALPHA)
        c_image.fill((255,0,0,80))
        f_image = pg.Surface((2*width, 2*length+2*self.properties['dash']), flags=pg.SRCALPHA)
        f_image.fill((255,0,0,80), pg.Rect(0, 0, 2*width, 2*length+self.properties['dash']))
        self.f_images = [c_image, self.image1, self.image2, f_image]
        self.c_images = [c_image, self.image1, self.image2]

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        self.owner.effects.append(effects.countdown_effect('busy', self.properties['before']+self.properties['duration'] + self.properties['after']))
        self.owner.effect_extend(effects.countdown_effect('unmovable', self.properties['before']+self.properties['duration']))
        match direction:
            case 'up':
                e = fields.Lunge(self.owner, 0, self.f_images, self.properties, dash = self.properties['dash'])
            case 'left':
                e = fields.Lunge(self.owner, 90, self.c_images, self.properties)
            case 'right':
                e = fields.Lunge(self.owner, -90, self.c_images, self.properties)
            case 'turn left':
                e = fields.Lunge(self.owner, 45, self.c_images, self.properties)
            case 'turn right':
                e = fields.Lunge(self.owner, -45, self.c_images, self.properties)
            case _:
                e = fields.Lunge(self.owner, 0, self.c_images, self.properties)
        self.owner.controller.fields.add(e)

class FastLunge(HeavyLunge):
    def update_properties(self, properties):
        origin = {'length': 48, 'width': 24, 'attack': 60, 'cd': 4, 'extension': 1, 'before': 1, 'duration': 5, 'after': 6, 'dash': 64}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        origin['length'] = properties.get('x_size', 1)*origin['length']
        origin['width'] = properties.get('x_size', 1)*origin['width']
        self.properties = origin
        length = self.properties['length']
        width = self.properties['width']
        self.image1 = pg.transform.scale(self.image1, (2*width, 2*length))
        self.image2 = pg.transform.scale(self.image2, (2*width, 2*length))
        c_image = pg.Surface((2*width, 2*length), flags=pg.SRCALPHA)
        c_image.fill((255,0,0,80))
        f_image = pg.Surface((2*width, 2*length+2*self.properties['dash']), flags=pg.SRCALPHA)
        f_image.fill((255,0,0,80), pg.Rect(0, 0, 2*width, 2*length+self.properties['dash']))
        self.f_images = [c_image, self.image1, self.image2, f_image]
        self.c_images = [c_image, self.image1, self.image2]

class Missile(Skill):
    def __init__(self, owner, properties = None):
        self.images = []
        self.images.append(util.load_image_alpha('skills/missile1.png'))
        self.images.append(util.load_image_alpha('skills/missile2.png'))
        self.images.append(util.load_image_alpha('skills/missile2.png'))
        field_image = pg.Surface((32, 32))
        pg.draw.circle(field_image, (255,0,0), (16, 16), 16)
        field_image.set_colorkey((0,0,0))
        field_image.set_alpha(80)
        self.field_image = field_image
        super().__init__(owner, properties)

    def update_properties(self, properties):
        origin = {'max_hp': 100, 'max_mp': 1, 'mp_regen': 0, 'speed': 4, 'size': 16, 'after': 12,
         'life': 1000, 'attack': 60, 'cd': 50, 'extension': 1.1, 'mp_consumption': 200, 'sense': 384, 'turn': 1}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*4
        self.images = [pg.transform.scale(image, (image_size, image_size)) for image in self.images]
        image_size = self.properties['size']*2*origin['extension']
        self.field_image = pg.transform.scale(self.field_image, (image_size, image_size))

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if any([effects.name == 'cd_Missile' for effects in self.owner.effects]):
            return
        if not self.consume_mp():
            return
        self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
        self.owner.effects.append(effects.countdown_effect('cd_Missile', self.properties['cd']))
        orientation = self.owner.orientation
        entity = entities.Missile(self.owner, self.images, self.owner.loc.copy(), orientation, self.properties)
        self.owner.controller.entities.add(entity)
        field = fields.MagicBullet(entity, self.field_image, self.properties)
        self.owner.controller.fields.add(field)

class FireBall(Skill):
    def __init__(self, owner, properties = None):
        self.images = []
        self.images.append(util.load_image_alpha('skills/fireball1.png'))
        self.images.append(util.load_image_alpha('skills/fireball2.png'))
        self.images.append(util.load_image_alpha('skills/fireball3.png'))
        field_image = pg.Surface((32, 32))
        pg.draw.circle(field_image, (255,0,0), (16, 16), 16)
        field_image.set_colorkey((0,0,0))
        field_image.set_alpha(80)
        self.field_image = field_image
        self.ex_image = util.load_image_alpha('skills/fireball_e.png')
        super().__init__(owner, properties)

    def update_properties(self, properties):
        origin = {'max_hp': 200, 'max_mp': 1, 'mp_regen': 0, 'speed': 4, 'size': 32, 'size2': 128, 'after': 20,
         'life': 150, 'attack': 20, 'attack2': 200, 'cd': 100, 'extension': 1.1, 'mp_consumption': 200}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        origin['attack2'] = properties.get('attack', 100)*origin['attack2']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        origin['size2'] = properties.get('x_size', 1)*origin['size2']
        self.properties = origin
        image_size = self.properties['size']*4
        self.images = [pg.transform.scale(image, (image_size, image_size)) for image in self.images]
        image_size = self.properties['size']*2*origin['extension']
        self.field_image = pg.transform.scale(self.field_image, (image_size, image_size))
        image_size = self.properties['size2']*2
        self.ex_image = pg.transform.scale(self.ex_image, (image_size, image_size))

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if any([effects.name == 'cd_FireBall' for effects in self.owner.effects]):
            return
        if not self.consume_mp():
            return
        self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
        self.owner.effects.append(effects.countdown_effect('cd_FireBall', self.properties['cd']))
        orientation = self.owner.orientation
        entity = entities.MagicBullet(self.owner, self.images, self.owner.loc.copy(), orientation, self.properties)
        self.owner.controller.entities.add(entity)
        field = fields.FireBall(entity, self.field_image, self.ex_image, self.properties)
        self.owner.controller.fields.add(field)

class Heal(Skill):
    def __init__(self, owner, properties = None):
        super().__init__(owner, properties)

    def update_properties(self, properties):
        origin = {'cd': 200, 'mp_consumption': 400, 'heal': 200}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if any([effects.name == 'cd_Heal' for effects in self.owner.effects]):
            return
        if not self.consume_mp():
            return
        self.owner.effects.append(effects.countdown_effect('cd_Heal', self.properties['cd']))
        self.owner.hp = min(self.owner.hp + self.properties['heal'], self.owner.max_hp)

class Healing(Skill):
    def __init__(self, owner, properties = None):
        super().__init__(owner, properties)

    def update_properties(self, properties):
        origin = {'cd': 50, 'mp_consumption': 300, 'heal': 2, 'benefit_time': 100}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if any([effects.name == 'cd_Healing' for effects in self.owner.effects]):
            return
        if not self.consume_mp():
            return
        self.owner.effects.append(effects.countdown_effect('cd_Healing', self.properties['cd']))
        self.owner.effect_extend(E.Healing(self.owner, self.properties))

class HelixCut(Skill):
    def __init__(self, owner, properties = None):
        image0 = util.load_image_alpha('skills/cut_f2.png')
        rect = image0.get_rect()
        image = pg.Surface(rect.size, flags=pg.SRCALPHA)
        pg.draw.arc(image, (255,0,0,80), rect, math.pi/4, math.pi/4*3, width=int(rect.w/2))
        image.blit(image0, (0, 0))
        self.image = image
        self.mark = None

        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'speed':0.4 ,'size': 96, 'attack': 40, 'extension': 1, 'after': 20}
        origin['speed'] = properties.get('speed', 5)*origin['speed']
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        self.image = pg.transform.scale(self.image, (image_size, image_size))

    def conduct(self, direction):
        if self.mark is None:
            if any([effects.name == 'busy' for effects in self.owner.effects]):
                return
            self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
            
            field = fields.HelixCut(self.owner, self.image, self.properties)
            effect = E.HelixCut(self.owner, field, self.properties)
            self.owner.controller.fields.add(field)
            self.owner.effects.append(effect)
            self.owner.properties['speed'] -= self.properties['speed']
            self.mark = effect
        else:
            self.mark.count = -1
            self.mark = None

    def stop(self):
        if self.mark is not None:
            self.mark.count = -1
            self.mark = None

class Transposition(Skill):
    def __init__(self, owner, properties = None):
        self.image = util.load_image_alpha('skills/transposition.png')
        self.mark = None
        super().__init__(owner, properties, accept_keys = ['down'])

    def update_properties(self, properties):
        origin = {'mp_consumption': 100, 'mp_consumption2': 200, 'cd': 100, 'after': 4}
        origin['mp_consumption'] = properties.get('x_mp_consumption', 1)*origin['mp_consumption']
        origin['mp_consumption2'] = properties.get('x_mp_consumption', 1)*origin['mp_consumption2']
        origin['cd'] = properties.get('x_cd', 1)*origin['cd']
        origin['after'] = properties.get('x_after', 1)*origin['after']
        self.properties = origin

    def conduct(self, direction):
        if direction == 'down':
            if any([effects.name == 'busy' for effects in self.owner.effects]):
                return
            if self.consume_mp():
                field = fields.Field(self.owner.controller, loc = self.owner.loc.copy(),
                 orientation = self.owner.orientation, image = self.image)
                self.owner.controller.fields.add(field)
                if self.mark is not None:
                    self.mark.kill()
                self.mark = field
        else:
            if self.mark is None:
                return
            if any([effects.name == 'busy' for effects in self.owner.effects]):
                return
            if any([effects.name == 'cd_Transposition' for effects in self.owner.effects]):
                return
            if self.consume_mp(self.properties['mp_consumption2']):
                self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
                self.owner.effects.append(effects.countdown_effect('cd_Transposition', self.properties['cd']))
                self.owner.loc = self.mark.loc.copy()
                self.owner.orientation = self.mark.orientation
            
class Laser(Skill):# unrecommended
    def __init__(self, owner, properties = None):
        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'mp_consumption': 100, 'attack': 100, 'width': 3, 'duration':6, 'after': 12}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if self.consume_mp():
            # begin to cast
            self.owner.effects.append(effects.countdown_effect('busy', self.properties['duration'] + self.properties['after']))
            self.owner.effects.append(effects.countdown_effect('unmovable', self.properties['duration']))
            field = fields.Laser(self.owner, 0, self.properties)
            self.owner.controller.fields.add(field)

class PenetrantLaser(Skill):
    def __init__(self, owner, properties = None):
        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'mp_consumption': 100, 'attack': 100, 'length': 32, 'width': 4, 'duration':6, 'after': 12}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        length = self.properties['length']
        width = self.properties['width']
        image0 = pg.Surface((2*width, 2*length), flags=pg.SRCALPHA)
        image0.fill((255,0,0))
        image0.set_alpha(80)
        image1 = pg.Surface((2*width, 2*length), flags=pg.SRCALPHA)
        image1.fill((255,255,255))
        self.images = [image0, image1]

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if self.consume_mp():
            # begin to cast
            self.owner.effects.append(effects.countdown_effect('busy', self.properties['duration'] + self.properties['after']))
            self.owner.effects.append(effects.countdown_effect('unmovable', self.properties['duration']))
            length = self.properties['length']
            for i in range(8):
                field = fields.PenetrantLaser(self.owner, pg.math.Vector2(length*(2*i+1), 0), 0, self.images, self.properties)
                self.owner.controller.fields.add(field)

class Billiard(Skill):
    def __init__(self, owner, properties = None):
        image1 = util.load_image_alpha('skills/billiard1.png')
        image2 = util.load_image_alpha('skills/billiard2.png')
        image3 = util.load_image_alpha('skills/billiard3.png')
        self.images = [image1, image2, image3]
        field_image = pg.Surface((32, 32))
        pg.draw.circle(field_image, (255,0,0), (16, 16), 16)
        field_image.set_colorkey((0,0,0))
        field_image.set_alpha(80)
        self.field_image = field_image
        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'max_hp': 50, 'max_mp': 1, 'mp_regen': 0, 'speed': 5, 'size': 16,
         'life': 1000, 'attack': 50, 'extension': 1.1, 'mp_consumption': 50, 'after': 12}
        origin['attack'] = properties.get('attack', 100)*origin['attack']/100
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        self.images = [pg.transform.scale(image, (image_size, image_size)) for image in self.images]
        image_size = self.properties['size']*2*origin['extension']
        self.field_image = pg.transform.scale(self.field_image, (image_size, image_size))

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if self.consume_mp():
            # begin to cast
            self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
            orientation = self.owner.orientation
            entity = entities.Billiard(self.owner, self.images, self.owner.loc.copy(), orientation, self.properties)
            self.owner.controller.entities.add(entity)
            field = fields.Billiard(entity, self.field_image, self.properties)
            self.owner.controller.fields.add(field)

class Bubble(Skill):
    def __init__(self, owner, properties = None):
        self.image = util.load_image_alpha('skills/bubble.png')
        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'max_hp': 1, 'max_mp': 1, 'mp_regen': 0, 'speed': 8, 'size': 32,
         'life': 200, 'mp_consumption': 10, 'after': 12}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        self.image = pg.transform.scale(self.image, (image_size, image_size))

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if self.consume_mp():
            # begin to cast
            self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
            orientation = self.owner.orientation
            entity = entities.Bubble(self.owner, orientation, self.image, self.properties)
            self.owner.controller.entities.add(entity)

class StoneColumn(Skill):
    def __init__(self, owner, properties = None):
        self.image = util.load_image_alpha('skills/stonecolumn.png')
        self.field_image = pg.Surface((32, 32))
        pg.draw.circle(self.field_image, (255,0,0), (16, 16), 16)
        self.field_image.set_colorkey((0,0,0))
        self.field_image.set_alpha(80)
        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'max_hp': 200, 'max_mp': 1, 'mp_regen': 0, 'size': 32, 'attack': 100,
         'mp_consumption': 200, 'after': 12, 'life': 24}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin
        image_size = self.properties['size']*2
        rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (image_size, image_size*rect.h/rect.w))
        self.field_image = pg.transform.scale(self.field_image, (image_size, image_size))

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if self.consume_mp():
            # begin to cast
            self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
            entity = entities.StoneColumn(self.owner, pg.math.Vector2(64, 0), self.image, self.properties)
            field = fields.StoneColumn(self.owner, entity, pg.math.Vector2(64, 0), self.field_image, self.properties)
            self.owner.controller.fields.add(field)

class AccelerateClocks(Skill):
    def __init__(self, owner, properties = None):
        #self.effect = None
        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'mp_consumption': 600, 'after': 12, 'benefit_time': 200, 'multiple': 2}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        origin['speed'] = properties['speed']*(origin['multiple']-1)
        origin['turn'] = properties['turn']*(origin['multiple']-1)
        self.properties = origin

    def conduct(self, direction):
        #if self.effect is None:
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if not self.consume_mp():
            return
        self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
        self.effect = E.AccelerateClocks(self.owner, self.properties)
        self.owner.effects.append(self.effect)
        self.owner.properties['speed'] += self.properties['speed']
        self.owner.properties['turn'] += self.properties['turn']
        self.owner.update_properties()
        #else:
            #self.effect.count = -1
            #self.effect = None

class StopClocks(Skill):
    def __init__(self, owner, properties = None):
        super().__init__(owner, properties, accept_keys = None)

    def update_properties(self, properties):
        origin = {'mp_consumption': 800, 'after': 12, 'benefit_time': 200}
        for property in origin:
            origin[property] = properties.get('x_' + property, 1)*origin[property]
        self.properties = origin

    def conduct(self, direction):
        if any([effects.name == 'busy' for effects in self.owner.effects]):
            return
        if not self.consume_mp():
            return
        self.owner.effects.append(effects.countdown_effect('busy', self.properties['after']))
        self.effect = E.StopClocks(self.owner, self.properties)
        self.owner.effects.append(self.effect)
        self.owner.controller.stop_clocks.sprite = self.owner

dictionary = {
    'Skill': Skill,
    'FastMove': FastMove,
    'MagicBullet': MagicBullet,
    'FastCut': FastCut,
    'HeavyCut': HeavyCut,
    'FastLunge': FastLunge,
    'HeavyLunge': HeavyLunge,
    'Missile': Missile,
    'FireBall': FireBall,
    'Heal': Heal,
    'Healing': Healing,
    'HelixCut': HelixCut,
    'Transposition': Transposition,
    'Laser': Laser,
    'PenetrantLaser': PenetrantLaser,
    'Billiard': Billiard,
    'Bubble': Bubble,
    'StoneColumn': StoneColumn,
    'AccelerateClocks': AccelerateClocks,#加速术
    'StopClocks': StopClocks,#时停
    'ToxicBall': Skill,#毒瓶
    'AcceleratingSpike': Skill,#加速针
    'Boomerang': Skill,#回旋镖
    'SuspendShield': Skill,#悬浮盾
    'SuspendSword': Skill,#悬浮剑
    'SuspendGrimoire': Skill,#悬浮魔导书
    'SpatialKnife': Skill,#空间刀
    'Vortex': Skill,#漩涡
    'SpawnSeeker': Skill,#召唤追踪者
    'SpawnTurret': Skill,#召唤炮塔
    'Portal': Skill,#传送门
    'Hook': Skill,#钩子
    'BlowOff': Skill,#吹飞
    'MagicShield': Skill,#魔法盾
    'Bump': Skill,#撞击
    'Lock': Skill,#封印
    'Telecontrol': Skill,#遥控
    'FireWall': Skill,#火墙
    'LandMine': Skill,#地雷
    'MindControl': Skill,#精神控制
    'Stealth': Skill#隐身
}