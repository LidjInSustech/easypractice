import json
import os
import pygame as pg

config = None
language = None

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

class Button():
    def __init__(self, text, rect):
        global language
        if text in language.keys():
            text = language[text]
        self.text = text
        self.rect = rect
        font = get_font(int(rect.height/2))
        font = font.render(text, True, (255,255,255), (0,0,0))
        font.set_colorkey((0,0,0))
        font_rect = font.get_rect()
        
        self.up_image = pg.Surface((rect.width, rect.height))
        self.up_image.fill((64,32,16))
        font_rect.center = self.up_image.get_rect().center
        self.up_image.blit(font, font_rect)

        self.down_image = pg.Surface((rect.width, rect.height))
        self.down_image.fill((32,64,128))
        self.down_image.blit(font, font_rect)