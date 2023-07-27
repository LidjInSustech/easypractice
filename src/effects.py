
class effect():
    def __init__(self, name):
        self.name = name
        
    def update(self):
        return True

    def __str__(self):
        return f'name: {self.name}'
    def __repr__(self):
        return self.__str__()

class countdown_effect(effect):
    def __init__(self, name, life):
        super().__init__(name)
        self.life = life

    def update(self):
        self.life -= 1
        return self.life > 0

    def __str__(self):
        return f'name: {self.name}, life: {self.life}'

class icon_effect(effect):
    def __init__(self, name, image):
        super().__init__(name)
        self.image = image

class icon_countdown_effect(icon_effect):
    def __init__(self, name, image, life):
        super().__init__(name, image)
        self.life = life

    def update(self):
        self.life -= 1
        return self.life > 0