import pygame as pg
import util
import skills.skills as skills

dictionary = {
    'Skill': skills.Skill,
    'FastMove': skills.FastMove,
    'MagicBullet': skills.MagicBullet,
    'FastCut': None,
    'HeavyCut': None,
    'Missile': None,
    'FireBall': None,
    'Heal': None,
    'Healing': None,
    'HelixCut': None,
    'Transposition': None
}

class Page(util.Rolling_Box):
    def __init__(self):
        global dictionary
        skill_names = list(dictionary.keys())
        self.skill_names = skill_names
        self.load_description()
        rect = pg.display.get_surface().get_rect()
        rect.width = rect.width//3
        button_rect = pg.Rect(0, 0, rect.width, rect.height*0.18)
        self.label_image = util.load_image('basic/label.png', button_rect)
        super().__init__(rect, button_rect, [self.description[i]['name'] for i in skill_names], util.load_image('basic/loading_page.png'))

    def draw(self):
        super().draw()
        self.screen.blit(plate, (rect.width*0.4, rect.height*0.05))
        pg.display.flip()

    def construct_plate(self):
        rect = self.screen.get_rect()
        plate = pg.Surface((rect.width*0.5, rect.height*0.9), pg.SRCALPHA)
        plate.fill((255,255,255,128))
        
        skill_image = pg.Surface((rect.h*0.3, rect.h*0.3))
        plate.blit(skill_image, (rect.w*0.5-rect.h*0.3-10, 10))
        plate.blit(self.label_image, (rect.w*0.5-self.button_rect.w-10, rect.h*0.35))

        font = util.get_font(32)
        font_rect = font.get_rect(self.description[self.skill_names[self.curser]]['name'])
        font_rect.center = (rect.w*0.5-self.button_rect.w-10 + self.button_rect.w/2, rect.h*0.35 + self.button_rect.h/2)
        font.render_to(plate, font_rect, self.description[self.skill_names[self.curser]]['name'], fgcolor=(251,254,110))

        font.render_to(plate, (rect.w*0.5-self.button_rect.w-10, rect.h*0.35 + self.button_rect.h), self.description[self.skill_names[self.curser]]['desc'], fgcolor=(251,254,110))
        return plate

    def load_description(self):
        self.description = util.load_text('skills')