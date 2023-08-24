import pygame as pg
import util

class Page(util.Rolling_Box):
    def __init__(self):
        self.label_names = ['up','down','left','right','turn left','turn right','fast mode','alter arm','skill1','skill2','skill3','skill4','skill5','skill6','interaction','default','confirm']
        self.read_config()
        screen = pg.display.get_surface()
        image = util.load_image('basic/loading_page.png', screen.get_size())
        rect = screen.get_rect()
        rect.move_ip(rect.width//2, 0)
        rect.width = rect.width//3
        button_rect = rect.copy()
        button_rect.height = 124
        self.lable_rect = rect.move(-rect.width, 0)
        super().__init__(rect, button_rect, self.translate_button_names(), picture = image)
        self.load_label(self.label_names)

    def load_label(self, label_names):
        image = util.load_image_alpha('basic/label.png', self.button_rect)
        self.labels = [util.Label(text, image) for text in label_names]

    def draw(self):
        super().draw()

        rolling_area = pg.Surface(self.rolling_rect.size, flags=pg.SRCALPHA)

        for i in range(len(self.labels)):
            rolling_area.blit(self.labels[i].image, (0, self.margin + i*(self.margin+self.button_rect.h)))
        start_pos = (self.rolling_rect.w, self.curser*(self.margin+self.button_rect.h))
        end_pos = (self.rolling_rect.w, start_pos[1] + self.margin*2 + self.button_rect.h)
                
        self.screen.blit(rolling_area, self.lable_rect, area=pg.Rect(0, self.offset*self.curser, self.rect.w, self.rect.h))
        pg.display.update(self.lable_rect)

    def start(self):
        message = super().start()
        while message != -1 and message != len(self.buttons) - 1:
            if message == len(self.buttons) - 2:
                self.default_config()
                self.button_names = self.translate_button_names()
                self.load_buttons(self.button_names)
                print(self.button_names)
                self.draw()
            else:
                if self.alter_key(message):
                    self.button_names = self.translate_button_names()
                    self.load_buttons(self.button_names)
                    print(self.button_names)
                    self.draw()
            message = super().start()

    def read_config(self):
        self.config = util.read_config('key_setting.json')
    
    def write_config(self):
        util.write_config('key_setting.json', self.config)

    def default_config(self):
        util.write_config('key_setting.json', util.read_config('key_default.json'))

    def translate_button_names(self):
        return [pg.key.name(name) for name in self.config.values()] + ['default', 'confirm']

    def alter_key(self, message):
        rect = self.screen.get_rect()
        rect.width = rect.width//2
        rect.height = rect.height//2
        rect.center = self.screen.get_rect().center
        wait_image = pg.Surface(rect.size)
        wait_image.fill((0,0,0))
        util.get_font(28).render_to(wait_image, (rect.width//4, rect.height//4), 'Press any key:', (50,220,220))
        self.screen.blit(wait_image, rect)
        pg.display.update(rect)

        event = pg.event.wait()
        while event.type != pg.KEYDOWN:
            event = pg.event.wait()

        if event.key == pg.K_ESCAPE:
            return False
        self.config[self.label_names[message]] = event.key
        self.write_config()
        return True
        event = pg.event.wait()