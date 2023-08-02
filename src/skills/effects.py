import effects as E

class Healing(E.countdown_effect):
    def __init__(self, owner, properties):
        self.life = properties.get('benefit_time', 100)
        self.heal = properties.get('heal', 2)
        self.owner = owner
        super().__init__('healing', life = self.life)

    def update(self):
        if super().update():
            self.owner.hp = min(self.owner.hp + self.heal, self.owner.max_hp)
            return True
        return False

class HelixCut(E.effect):
    def __init__(self, owner, field, properties):
        self.speed = properties.get('speed', 3)
        self.owner = owner
        self.field = field
        self.count = 4
        super().__init__('helix_cut')

    def update(self):
        if self.count < 0:
            self.owner.properties['speed'] += self.speed
            self.field.kill()
            return False
        self.count -= 1
        if self.count == 0:
            self.count = 4
            self.owner.effect_extend(E.countdown_effect('busy', life = 4))
        return True

class AccelerateClocks(E.countdown_effect):
    def __init__(self, owner, properties):
        self.addition = properties.get('multiple', 2) - 1
        self.owner = owner
        self.count = self.addition 
        life = properties.get('benefit_time', 100)
        self.mp_consumption = properties.get('mp_consumption', 3)
        self.roll_back = False
        self.properties = properties
        super().__init__('accelerate_clocks', life = life)

    def update(self):
        if self.owner.mp < self.mp_consumption:
            self.life = 0
            return False
        self.owner.mp -= self.mp_consumption
        # start
        if super().update():
            if self.count > 0:
                self.count -= 1
                self.owner.update()
            else:
                self.count += self.addition
                self.owner.controller.flamerate = 15
            return True
        if not self.roll_back:
            self.owner.properties['speed'] -= self.properties['speed']
            self.owner.properties['turn'] -= self.properties['turn']
            self.owner.update_properties()
            self.roll_back = True
        return False

class StopClocks(E.countdown_effect):
    def __init__(self, owner, properties):
        self.owner = owner
        self.mp_consumption = properties.get('mp_consumption', 3)
        super().__init__('stop_clocks', life = properties.get('benefit_time', 200))

    def update(self):
        if super().update() and self.owner.mp >= self.mp_consumption:
            self.owner.mp -= self.mp_consumption
            return True
        self.owner.controller.stop_clocks.empty()
        return False