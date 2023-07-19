import entities
import util
import skills
import math
import random
import effects

def load_game(CORE):
    hero_skills = [skills.fast_move(), skills.slow_cut(), skills.magic_sperm(), skills.basic(), skills.basic(), skills.basic(), skills.basic()]
    hero = entities.Prepared_entity(CORE, hero_skills, picture=util.load_image_alpha('entities/human0.png', 64, 64))
    hero.party = 1
    enemy = test_enemy(CORE)
    enemy.party = 2
    backgroundimage = util.load_image('floor/colorful.png', 1024, 1024, (0,0,0))
    CORE.load(backgroundimage, hero, [enemy])
    CORE.start()

class test_enemy(entities.Prepared_entity):
    def __init__(self, core):
        picture = util.load_image_alpha('entities/human1.png', 64, 64)
        super().__init__(core, [skills.slow_cut()], x = 500, y = 0, picture = picture)
        self.thought = 'seek'

    def update(self):
        xx, yy = self.core.hero.loc_x-self.loc_x, self.core.hero.loc_y-self.loc_y
        mesure = math.sqrt(xx**2+yy**2)
        if mesure > 280:
            self.thought = 'seek'
        else:
            self.orient = math.degrees(math.atan2(yy, xx))
            if self.thought == 'seek':
                self.thought = 'alert'
            if self.thought == 'alert':
                if random.random() < 0.01:
                    self.thought = 'attack'
        self.action(mesure)
            

        super().update()

    def action(self, mesure):
        if self.thought == 'seek':
            if random.random() < 0.95:
                self.effects.append(effects.simple_forward(self, 5))
            else:
                self.orient = random.random()*360
        elif self.thought == 'alert':
            if mesure < 120:
                self.effects.append(effects.simple_forward(self, -5))
            elif mesure > 160:
                self.effects.append(effects.simple_forward(self, 5))
            else:
                self.effects.append(effects.simple_slide(self, 5))
        elif self.thought == 'attack':
            if mesure > 100:
                self.effects.append(effects.simple_forward(self, 5))
            else:
                self.skills[0].act(self, 'F')
                self.thought = 'alert'
        else:
            raise Exception('iligal thought')


