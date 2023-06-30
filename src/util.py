import json
import os
import pygame as pg

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
    return pg.font.SysFont('Calibri', size)

class Button():
    def __init__(self, text, rect):
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