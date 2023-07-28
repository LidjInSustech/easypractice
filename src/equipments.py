import util

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
                    player.properties[key] = player.properties.get(key, 1) + value
                    self.record[key] = value
                case 'proportion':
                    if key not in player.properties:
                        player.properties[key] = 1
                    value_ = player.properties[key] * value
                    player.properties[key] += value_
                    self.record[key] = value_
        self.equipped = True

    def unequip(self, player):
        if not self.equipped:
            return
        for key, value in self.record.items():
            player.properties[key] -= value
        self.equipped = False

def load():
    return util.load_data('equipments')

def get_weapon(name):
    try:
        return equipment(name, load()['weapons'][name])
    except KeyError:
        return equipment('empty', load()['weapons']['empty'])

def get_equipment(name):
    try:
        return equipment(name, load()['equipments'][name])
    except KeyError:
        return None
