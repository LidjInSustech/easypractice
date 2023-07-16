import json
import os
import pygame as pg

config = None
language = None
loading_image = None

def init():
    global font, config, language
    config = read_config('config.json')
    if config['language'] == 'en':
        language = {}
    else:
        with open('data/lang/{}.json'.format(config['language']), 'r') as f:
            language = json.load(f)

def get_word(text):
    global language
    if text in language.keys():
        return language[text]
    else:
        return text

def read_config(filename):
    filename = os.path.join('configure', filename)
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

def write_config(filename, config):
    filename = os.path.join('configure', filename)
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)
    return config

def get_font(size):
    try:
        return pg.font.SysFont(config['font'], int(size*config['font_size']))
    except:
        return pg.font.SysFont('Calibri', size)

def load_image(filename, hight, width, colorkey=None):
    filename = os.path.join('res', filename)
    try:
        image = pg.image.load(filename)
    except pg.error:
        print('Cannot load image:', filename)
        raise SystemExit(str(get_word('Could not load image')))
        return None
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    image = pg.transform.scale(image, (hight, width))
    return image

def load_image_alpha(filename, hight, width):
    filename = os.path.join('res', filename)
    try:
        image = pg.image.load(filename)
    except pg.error:
        print('Cannot load image:', filename)
        raise SystemExit(str(get_word('Could not load image')))
        return None
    image = image.convert_alpha()
    image = pg.transform.scale(image, (hight, width))
    return image

def loading_page():
    global loading_image
    if loading_image == None:
        loading_image = load_image('basic/loading_page.png', pg.display.get_surface().get_width(), pg.display.get_surface().get_height())
        if loading_image == None:
            loading_image = pg.Surface((pg.display.get_surface().get_width(), pg.display.get_surface().get_height()))
        font = get_font(32)
        #loading_image = font.render(get_word('loading...'), True, (50, 100, 150))
        loading_image.blit(font.render(get_word('loading...'), True, (50, 100, 150)), (20,20))
    pg.display.get_surface().blit(loading_image, (0,0))
    pg.display.update()


class Button():
    def __init__(self, text, rect):
        global language
        if text in language.keys():
            text = language[text]
        self.text = text
        self.rect = rect
        font = get_font(int(rect.height/2))
        font = font.render(text, True, (251,254,110), (0,0,0))
        font.set_colorkey((0,0,0))
        font_rect = font.get_rect()
        
        self.up_image = load_image_alpha('basic/button_up.png', rect.width, rect.height)
        if self.up_image is None:
            self.up_image = pg.Surface((rect.width, rect.height))
            self.up_image.fill((64,32,16))
        font_rect.center = self.up_image.get_rect().center
        self.up_image.blit(font, font_rect)

        self.down_image = load_image_alpha('basic/button_down.png', rect.width, rect.height)
        if self.down_image is None:
            self.down_image = pg.Surface((rect.width, rect.height))
            self.down_image.fill((32,64,128))
        self.down_image.blit(font, font_rect)

class Button_Box():
    def __init__(self, rect, button_names, picture=None):
        self.screen = pg.display.get_surface()
        self.rect = rect
        self.curser = 0
        self.load_buttons(button_names)
        self.picture = picture

    def draw(self):
        self.screen.fill((0,0,0))
        if self.picture is not None:
            self.screen.blit(self.picture, self.picture.get_rect())
        for button in self.buttons:
            self.screen.blit(button.up_image, button.rect)
        self.screen.blit(self.buttons[self.curser].down_image, self.buttons[self.curser].rect)
        pg.display.update()

    def load_buttons(self, button_names):
        margin = 10
        width = (self.rect.width - margin)//2 - margin
        height = (self.rect.height - margin)//len(button_names) - margin

        self.buttons = []
        for row in range(len(button_names)):
            self.buttons.append(Button(button_names[row], pg.Rect(margin, margin + (height + margin) * row, width, height)))

    def start(self):
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
                    if event.key == pg.K_RETURN:
                        self.running = False
                        return self.curser

class Menu_Page(Button_Box):
    def __init__(self, button_names, picture, picture_rect):
        rect = pg.display.get_surface().get_rect()
        rect.width = rect.width // 2
        super().__init__(rect, button_names)
        self.picture = picture
        self.picture_rect = picture_rect

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.picture, self.picture_rect)
        super().draw()
