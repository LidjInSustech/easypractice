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
