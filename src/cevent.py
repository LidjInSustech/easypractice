import pygame as pg

ATTACK = None
LIFE_BORN = None
LIFE_KILL = None

def init():
    global ATTACK
    global LIFE_BORN
    global LIFE_KILL
    ATTACK = pg.event.custom_type()
    LIFE_BORN = pg.event.custom_type()
    LIFE_KILL = pg.event.custom_type()