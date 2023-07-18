import pygame as pg
import util

class skills_setting(util.Rolling_Box):
    def __init__(self):
        surface_rect = pg.display.get_surface().get_rect()
        picture = util.load_image('basic/loading_page.png', surface_rect.width, surface_rect.height)

        registered_skills = ['basic', 'fast_move', 'slow_cut', 'magic_sperm']

        super().__init__(surface_rect, pg.Rect(0,0,surface_rect.width//2,surface_rect.height//8), registered_skills, picture)