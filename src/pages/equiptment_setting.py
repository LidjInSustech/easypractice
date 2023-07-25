import pygame as pg
import util
import equipments
from pages.skill_setting import infomation_plane

class Page(util.Rolling_Box):
    def __init__(self):
        rect = pg.display.get_surface().get_rect()
        self.image = util.load_image('basic/loading_page.png', rect)
        rect.width = rect.width//3
        button_rect = pg.Rect(0, 0, rect.width, rect.height*0.18)
        super().__init__(rect.copy(), button_rect, ['weapon', 'equipment'])
        self.load_description()
        self.load_player()
        weapon_names = list(self.description['weapons'].keys())
        self.weapon_box = util.Rolling_Box(rect.move(rect.width, 0), button_rect, [self.description['weapons'][i]['name'] for i in weapon_names])
        self.weapon_box.description = self.description['weapons']
        self.weapon_box.names = weapon_names
        equipment_names = list(self.description['equipments'].keys())
        self.equipment_box = util.Rolling_Box(rect.move(rect.width, 0), button_rect, [self.description['equipments'][i]['name'] for i in equipment_names])
        self.equipment_box.description = self.description['equipments']
        self.equipment_box.names = equipment_names
        self.subbox = [self.weapon_box, self.equipment_box]
        self.plane = infomation_plane(rect.move(rect.width*2, 0))
        self.site = self

    def draw(self):
        self.screen.blit(self.image, self.image.get_rect())
        pg.draw.rect(self.screen, (251,254,110), self.site.rect, 3)
        super().draw()
        self.subbox[self.curser].draw()
        names = self.subbox[self.curser].names
        name = self.subbox[self.curser].description[names[self.subbox[self.curser].curser]]['name']
        icon = pg.Surface((64, 64))
        desc = self.subbox[self.curser].description[names[self.subbox[self.curser].curser]]['desc']
        playerinfo = self.get_player_info()
        self.plane.draw(name, icon, desc, playerinfo)
        pg.display.flip()

    def start(self):
        self.screen.blit(self.image, (0, 0))
        self.running = True
        clock = pg.time.Clock()
        while self.running:
            clock.tick(20)
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    return -1
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        return -1
                    if event.key == pg.K_DOWN:
                        self.site.curser = (self.site.curser + 1) % len(self.site.buttons)
                    if event.key == pg.K_UP:
                        self.site.curser = (self.site.curser - 1) % len(self.site.buttons)
                    if event.key in(pg.K_RETURN, pg.K_RIGHT):
                        if self.site == self:
                            self.site = self.subbox[self.curser]
                        elif self.curser == 0:
                            rect = pg.display.get_surface().get_rect()
                            chossing = util.Button_Box(pg.Rect(rect.w/3, rect.h/3, rect.w/3, rect.h/3), ['primary weapon', 'sub weapon'], self.image)
                            chossing = chossing.start()
                            if chossing == 0:
                                self.player['primary weapon']['name'] = self.weapon_box.names[self.weapon_box.curser]
                                self.save_player()
                            if chossing == 1:
                                self.player['sub weapon']['name'] = self.weapon_box.names[self.weapon_box.curser]
                                self.save_player()
                        elif self.curser == 1:
                            if self.equipment_box.names[self.equipment_box.curser] in self.player['equipments']:
                                self.player['equipments'].remove(self.equipment_box.names[self.equipment_box.curser])
                                self.save_player()
                            else:
                                self.player['equipments'].append(self.equipment_box.names[self.equipment_box.curser])
                                self.save_player()
                    if event.key == pg.K_LEFT:
                        if self.site != self:
                            self.site = self

    def load_description(self):
        self.description = util.load_text('equipments')
        self.properties = equipments.load()

    def load_player(self):
        self.player = util.read_config('player.json')

    def save_player(self):
        util.write_config('player.json', self.player)

    def get_player_info(self):
        info = ['']
        if self.curser == 0:
            info.append(util.get_word('weapon'))
            names = self.weapon_box.names
            for line in self.properties['weapons'][names[self.weapon_box.curser]]:
                info.append(self.translate(line))
            info.append('')
            if self.player['primary weapon']['name'] == names[self.weapon_box.curser]:
                info.append(util.get_word('primary weapon'))
            if self.player['sub weapon']['name'] == names[self.weapon_box.curser]:
                info.append(util.get_word('sub weapon'))
        elif self.curser == 1:
            info.append(util.get_word('equipment'))
            names = self.equipment_box.names
            for line in self.properties['equipments'][names[self.equipment_box.curser]]:
                info.append(self.translate(line))
            info.append('')
            if names[self.equipment_box.curser] in self.player['equipments']:
                info.append('equipped')
        return info

    @staticmethod
    def translate(tup):
        key, operon, value = tup
        if operon == 'plus':
            return f'{key} + {value}'
        elif operon == 'proportion':
            return f'{key} + {key} X {value}'