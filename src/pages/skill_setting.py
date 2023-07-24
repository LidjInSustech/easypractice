import pygame as pg
import util

class Page(util.Rolling_Box):
    def __init__(self):
        skill_names = ['BasicSkill', 'FastMove']
        rect = pg.display.get_surface().get_rect()
        rect.width = rect.width//2
        button_rect = pg.Rect(0, 0, rect.width, rect.height*0.25)
        super().__init__(rect, button_rect, skill_names, util.load_image('basic/loading_page.png'))