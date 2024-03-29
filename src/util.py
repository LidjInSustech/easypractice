import json
import os
import pygame as pg
import pygame.freetype as ftype

config = None
trans_table = None
loading_image = None
font = None

def init():
    global config, trans_table
    config = read_config('config.json')
    trans_table = load_text('words')
    ftype.init()

def load_text(filename):
    global config
    with open('data/lang/{}/{}.json'.format(config['language'], filename), 'r', encoding='utf8') as f:
        return json.load(f)

def load_data(filename):
    with open('data/{}.json'.format(filename), 'r', encoding='utf8') as f:
        return json.load(f)

def get_word(text):
    global trans_table
    words = trans_table
    if text in words.keys():
        return words[text]
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
    global font
    if font is None:
        try:
            font = ftype.SysFont(config['font_style'], int(size*config['font_size']))
        except:
            font = ftype.SysFont(None, size)
    font.size = size
    return font

def load_image(filename, rect = None, colorkey = None):
    filename = os.path.join('res', filename)
    if isinstance(rect, pg.Rect):
        rect = rect.size

    try:
        image = pg.image.load(filename)
    except pg.error:
        print('Cannot load image:', filename)
        raise SystemExit(str(get_word('Could not load image')))
        return None

    if rect is not None:
        image = pg.transform.scale(image, rect)

    image = image.convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)

    return image

def load_image_alpha(filename, rect = None):
    filename = os.path.join('res', filename)
    if isinstance(rect, pg.Rect):
        rect = rect.size

    try:
        image = pg.image.load(filename)
    except pg.error:
        print('Cannot load image:', filename)
        raise SystemExit(str(get_word('Could not load image')))
        return None

    if rect is not None:
        image = pg.transform.scale(image, rect)

    return image.convert_alpha()

def show_loading_page():
    global loading_image
    if loading_image == None:
        loading_image = load_image('basic/loading_page.png', pg.display.get_surface().get_rect())
        get_font(32).render_to(loading_image, (100, 100), get_word('loading...'), (50, 100, 150))
    pg.display.get_surface().blit(loading_image, (0,0))
    pg.display.update()


class Button():
    def __init__(self, text, images):
        global trans_table
        text = get_word(text)
        rect = images[0].get_rect()

        font = get_font(int(rect.height/2))
        font_rect = font.get_rect(text)
        font_rect.center = rect.center
        self.up = images[0].copy()
        font.render_to(self.up, font_rect, text, (251,254,110))
        self.down = images[1].copy()
        font.render_to(self.down, font_rect, text, (251,254,110))

class Label():
    def __init__(self, text, image):
        global trans_table
        text = get_word(text)
        rect = image.get_rect()

        font = get_font(int(rect.height/2))
        font_rect = font.get_rect(text)
        font_rect.center = rect.center
        self.image = image.copy()
        font.render_to(self.image, font_rect, text, (251,254,110))

class Button_Box():
    def __init__(self, rect, button_names, picture=None, margin=10):
        self.screen = pg.display.get_surface()
        self.rect = rect
        self.curser = 0
        self.load_buttons(button_names, margin)
        self.picture = picture
        self.button_names = button_names
        self.margin = margin

    def load_buttons(self, button_names, margin):
        button_width = (self.rect.width - margin) - margin
        button_height = (self.rect.height - margin)//len(button_names) - margin
        button_rect = pg.Rect(0, 0, button_width, button_height)

        self.up_image = load_image_alpha('basic/button_up.png', button_rect)
        self.down_image = load_image_alpha('basic/button_down.png', button_rect)
        self.button_rect = button_rect
        self.buttons = [Button(text, (self.up_image, self.down_image)) for text in button_names]

    def draw(self):
        if self.picture is not None:
            self.screen.blit(self.picture, self.picture.get_rect())

        for i in range(self.curser):
            self.screen.blit(self.buttons[i].up, (self.rect.x, self.rect.y+self.margin + i*(self.margin+self.button_rect.h)))
        self.screen.blit(self.buttons[self.curser].down, (self.rect.x, self.rect.y+self.margin + self.curser*(self.margin+self.button_rect.h)))
        for i in range(self.curser+1, len(self.buttons)):
            self.screen.blit(self.buttons[i].up, (self.rect.x, self.rect.y+self.margin + i*(self.margin+self.button_rect.h)))

        pg.display.update(self.rect)

    def start(self):
        if self.picture is not None:
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
                    if event.key == pg.K_RETURN:
                        self.running = False
                        return self.curser

class Rolling_Box(Button_Box):
    def __init__(self, rect, button_rect, button_names, picture=None, margin=10):
        self.margin = margin
        self.screen = pg.display.get_surface()
        self.rolling_rect = pg.Rect(0, 0, button_rect.w, (button_rect.h+margin)*len(button_names))
        rect.h = min(rect.h, self.rolling_rect.height)
        self.rect = rect
        self.button_rect = button_rect
        self.curser = 0
        self.load_buttons(button_names)
        self.picture = picture
        self.offset = (self.rolling_rect.height - self.rect.height) / (len(self.buttons) - 1)
        self.scrollbar_len = self.rect.height * self.rect.height / self.rolling_rect.height

    def load_buttons(self, button_names):
        self.up_image = load_image_alpha('basic/button_up.png', self.button_rect)
        self.down_image = load_image_alpha('basic/button_down.png', self.button_rect)
        self.buttons = [Button(text, (self.up_image, self.down_image)) for text in button_names]

    def draw(self):
        if self.picture is not None:
            self.screen.blit(self.picture, self.picture.get_rect())

        rolling_area = pg.Surface(self.rolling_rect.size, flags=pg.SRCALPHA)

        for i in range(self.curser):
            rolling_area.blit(self.buttons[i].up, (0, self.margin + i*(self.margin+self.button_rect.h)))
        rolling_area.blit(self.buttons[self.curser].down, (0, self.margin + self.curser*(self.margin+self.button_rect.h)))
        for i in range(self.curser+1, len(self.buttons)):
            rolling_area.blit(self.buttons[i].up, (0, self.margin + i*(self.margin+self.button_rect.h)))
        start_pos = (self.rolling_rect.w, self.offset*self.curser + (self.rect.h - self.scrollbar_len) * self.curser / (len(self.buttons) - 1))
        end_pos = (self.rolling_rect.w, start_pos[1] + self.scrollbar_len)
        pg.draw.line(rolling_area, (251,254,110), start_pos, end_pos, self.margin)
        
        self.screen.blit(rolling_area, self.rect, area=pg.Rect(0, self.offset*self.curser, self.rect.w, self.rect.h))
        pg.display.update(self.rect)

def load_sound(filename):
    class NoneSound:
        def play(self):
            pass
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    sound = pg.mixer.Sound(filename)
    return sound