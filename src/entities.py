import pygame as pg
import visibles
import equipments
import util
import automixin
from skills.skills import dictionary

class Player(visibles.Movable):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, image = None, radius = None):
        player = util.read_config('player.json')
        super().__init__(controller, loc = loc, orientation = orientation, faction = 1,
         image = image, radius = radius, rotate_image = False, properties = player['properties'])
        self.equipments = [equipments.get_equipment(name) for name in player['equipments']]
        for equipment in self.equipments:
            equipment.equip(self)
        primary_weapon = equipments.get_weapon(player['primary weapon']['name'])
        sub_weapon = equipments.get_weapon(player['sub weapon']['name'])
        self.weapons = [primary_weapon, sub_weapon]
        self.weaponnum = 0
        self.weapons[1].skills = [dictionary['FastMove'](self)] + [dictionary[skill_name](self) for skill_name in player['sub weapon']['skills']]
        self.weapon.equip(self)
        self.weapons[0].skills = [dictionary['FastMove'](self)] + [dictionary[skill_name](self) for skill_name in player['primary weapon']['skills']]

    @property
    def weapon(self):
        return self.weapons[self.weaponnum]

    def switch_weapon(self):
        self.weapon.unequip(self)
        for skill in self.weapon.skills:
            skill.stop()
        self.weaponnum = 1 - self.weaponnum
        self.weapon.equip(self)
        for skill in self.weapon.skills:
            skill.update_properties(self.properties)
        
class RandomWalk(visibles.Movable, automixin.Patrol):
    def __init__(self, controller, loc = pg.math.Vector2(), orientation = 0, image = None, radius = None):
        super().__init__(controller, loc = loc, orientation = orientation, faction = 2,
         image = image, radius = radius, rotate_image = False)
        self.set_path([pg.math.Vector2(100, 0), pg.math.Vector2(-100, 0)])

    def update(self):
        self.free()
        super().update()