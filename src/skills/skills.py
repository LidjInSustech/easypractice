import pygame as pg
import util
import visibles
import skills.entities as entities
import skills.fields as fields
import effects

class Skill():
    def __init__(self, owner, properties = None, accept_keys = None):
        self.owner = owner
        if properties is None:
            properties = {}
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

class FastMove(Skill):
    def __init__(self, owner, properties = None):
        self.image = pg.Surface((64, 64))
        pg.draw.line(self.image, (255,255,255), (32, 32), (32, 64), width = 4)
        self.image.set_colorkey((0,0,0))
        self.icon = util.load_image('effects/unstable.png')
        accept_keys = ['up', 'down', 'left', 'right', 'turn left', 'turn right']
        super().__init__(owner, properties, accept_keys)
        
    def update_properties(self, properties):
        default = {'speed': 20, 'cd': 12, 'time': 4}
        self.speed = properties.get('speed', self.owner.speed)*default['speed']
        self.cd = properties.get('cd', 1)*default['cd']
        self.time = properties.get('time', 1)*default['time']
        self.image = pg.transform.scale(self.image, (self.speed*2, self.speed*2))

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
        self.owner.effects.append(effects.icon_countdown_effect('unstable', self.icon, self.cd))
        orientation += self.owner.orientation
        self.owner.loc += pg.math.Vector2(1, 0).rotate(orientation)*self.speed
        self.owner.controller.fields.add(fields.FastMove(self.owner, orientation, image = self.image))
        for e in self.owner.effects:
            if e.name == 'invincible':
                e.time += self.time
                return
        self.owner.effects.append(effects.countdown_effect('invincible', self.time))

class MagicBullet(Skill):
    def __init__(self, owner, properties = None):
        self.images = []
        self.images.append(util.load_image_alpha('skills/mag_sperm.png'))
        self.images.append(util.load_image_alpha('skills/mag_sperm1.png'))
        self.images.append(util.load_image_alpha('skills/mag_sperm2.png'))
        field_image = pg.Surface((32, 32))
        pg.draw.circle(field_image, (255,0,0), (16, 16), 16)
        field_image.set_colorkey((0,0,0))
        field_image.set_alpha(128)
        self.field_image = field_image
        super().__init__(owner, properties)

    def update_properties(self, properties):
        default = {'max_hp': 100, 'speed': 1, 'size': 32, 'life': 100, 'damage': 100, 'cd': 1, 'extension': 4}
        self.max_hp = properties.get('max_hp', 1)*default['max_hp']
        self.speed = properties.get('speed', 5)*default['speed']
        self.size = properties.get('size', 1)*default['size']
        self.life = properties.get('life', 1)*default['life']
        self.damage = properties.get('damage', 1)*default['damage']
        self.cd = properties.get('cd', 1)*default['cd']
        self.extension = properties.get('extension', 1)*default['extension']
        self.images = [pg.transform.scale(image, (self.size, self.size)) for image in self.images]
        self.field_image = pg.transform.scale(self.field_image, (self.size+self.extension, self.size+self.extension))

    def conduct(self, direction):
        if any([effects.name == 'spell_cd' for effects in self.owner.effects]):
            return
        self.owner.effects.append(effects.countdown_effect('spell_cd', self.cd))
        orientation = self.owner.orientation
        entity_properties = {'max_hp': self.max_hp, 'max_mp':0, 'mp_regen':0, 'speed': self.speed, 'size': self.size, 'life': self.life}
        entity = entities.MagicBullet(self.owner, self.images, self.owner.loc.copy(), orientation, entity_properties)
        self.owner.controller.entities.add(entity)
        field_properties = {'size': self.size, 'extension': self.extension, 'damage': self.damage}
        field = fields.MagicBullet(entity, self.field_image, field_properties)
        self.owner.controller.fields.add(field)
        
