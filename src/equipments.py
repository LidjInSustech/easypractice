import util

def load():
    return util.load_data('equipments')

def get_equipment(name, weapon = False):
    if weapon:
        return equipment(name, equipments['weapon'][name])
    else:
        return equipment(name, equipments['equipment'][name])

class equipment():
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties
        self.equipped = False
        self.record = {}

    def equip(self, player):
        if self.equipped:
            return
        for key, operon, value in self.properties:
            match operon:
                case 'plus':
                    player.properties[key] += value
                    self.record[key] = value
                case 'proportion':
                    value_ = player.properties[key] * value
                    player.properties[key] += value_
                    self.record[key] = value_
        self.equipped = True

    def unequip(self, player):
        if not self.equipped:
            return
        for key, value in self.record:
            player.properties[key] -= value
        self.equipped = False