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
        self.properties = properties
        self.accept_keys = accept_keys

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
        accept_keys = ['up', 'down', 'left', 'right', 'turn left', 'turn right']
        super().__init__(owner, properties, accept_keys)
        if 'speed' not in self.properties:
            speed = self.owner.speed*20
        else:
            speed = self.properties['speed']
        if 'cd' not in self.properties:
            self.cd = 12
        else:
            self.cd = self.properties['cd']
        self.image = pg.Surface((speed*2, speed*2))
        pg.draw.line(self.image, (255,255,255), (speed, speed), (speed, speed*2), width = 4)
        self.speed = speed
        self.image.set_colorkey((0,0,0))
        self.icon = util.load_image('effects/unstable.png')

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
        if any([effects.name == 'unstable' for effects in self.owner.effects]):
            return
        self.owner.effects.append(effects.icon_countdown_effect('unstable', self.icon, self.cd))
        orientation += self.owner.orientation
        self.owner.loc += pg.math.Vector2(1, 0).rotate(orientation)*self.speed
        self.owner.controller.fields.add(fields.FastMove(self.owner, orientation, image = self.image))