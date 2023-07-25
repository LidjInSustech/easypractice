import pygame as pg
import util

class Page(util.Rolling_Box):
    def __init__(self):
        self.label_names = ['language', 'font_style', 'font_size', 'confirm']
        self.read_config()
        screen = pg.display.get_surface()
        image = util.load_image('basic/loading_page.png', screen.get_size())
        rect = screen.get_rect()
        rect.move_ip(rect.width//2, 0)
        rect.width = rect.width/5*2
        button_rect = rect.copy()
        button_rect.height = 124
        self.lable_rect = rect.move(-rect.width, 0)
        self.create_items()
        super().__init__(rect, button_rect, self.get_button_names(), picture = image)
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
        self.screen.blit(self.picture, self.picture.get_rect())
        pg.display.flip()
        self.running = True
        clock = pg.time.Clock()
        while self.running:
            clock.tick(60)
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
                        self.curser = (self.curser + 1) % len(self.buttons)
                    if event.key == pg.K_UP:
                        self.curser = (self.curser - 1) % len(self.buttons)
                    if event.key == pg.K_RETURN and self.curser == len(self.buttons) - 1:
                        self.running = False
                        self.write_config()
                        return self.curser
                    if self.curser < len(self.buttons) - 1:
                        if event.key == pg.K_LEFT:
                            self.indexies[self.curser] = (self.indexies[self.curser] - 1) % len(self.items[self.curser])
                        if event.key == pg.K_RIGHT:
                            self.indexies[self.curser] = (self.indexies[self.curser] + 1) % len(self.items[self.curser])
                        item = self.items[self.curser][self.indexies[self.curser]]
                        self.config[self.label_names[self.curser]] = item
                        util.config[self.label_names[self.curser]] = item
                        self.buttons[self.curser] = util.Button(str(item), (self.up_image, self.down_image))

    def read_config(self):
        self.config = util.config.copy()
    
    def write_config(self):
        util.write_config('config.json', self.config)
        util.config = self.config

    def create_items(self):
        indexies = []
        language = ['cn', 'en']
        indexies.append(language.index(self.config['language']))
        font_style = pg.font.get_fonts()
        try:
            indexies.append(font_style.index(self.config['font_style']))
        except ValueError:
            indexies.append(0)
        font_size = [i*0.1 for i in range(1, 30, 1)]
        indexies.append(font_size.index(self.config['font_size']))
        self.items = [language, font_style, font_size]
        self.indexies = indexies

    def get_button_names(self):
        return [str(self.items[i][index]) for i, index in enumerate(self.indexies)] + ['confirm']