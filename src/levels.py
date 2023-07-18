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
        super().__init__(core, [skills.slow_cut()], x = 500, y = 500, picture = picture)

    def update(self):
        xx, yy = self.core.hero.loc_x-self.loc_x, self.core.hero.loc_y-self.loc_y
        self.orient = math.degrees(math.atan2(yy, xx))
        if xx**2+yy**2 < 60**2:
            if random.random() < 0.6:
                self.effects.append(effects.simple_slide(self, -5))
            else:
                self.random_walk()
        elif xx**2+yy**2 < 120**2:
            if random.random() < 0.6:
                self.skills[0].act(self, 'F')
            else:
                self.random_walk()
        else:
            if random.random() < 0.8:
                self.effects.append(effects.simple_forward(self, 5))
            else:
                self.random_walk()

        super().update()

    def random_walk(self):
        value = random.random()
        if value < 0.6:
            return
        elif value < 0.7:
            self.effects.append(effects.simple_forward(self, -5))
        elif value < 0.8:
            self.effects.append(effects.simple_slide(self, 5))
        elif value < 0.9:
            self.effects.append(effects.simple_slide(self, -5))
        else:
            self.skills[0].act(self, 'F')
