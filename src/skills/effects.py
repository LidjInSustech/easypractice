import effects as E

class Healing(E.countdown_effect):
    def __init__(self, owner, properties):
        self.life = properties.get('benefit_time', 100)
        self.heal = properties.get('heal', 2)
        self.owner = owner
        super().__init__('healing', life = self.life)

    def update(self):
        super().update()
        self.owner.hp = min(self.owner.hp + self.heal, self.owner.max_hp)

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
            self.owner.effect_extend(E.countdown_effect('unstable', life = 4))
            self.owner.effect_extend(E.countdown_effect('sword_cd', life = 4))
        return True