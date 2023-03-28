import pygame as pg

class Key_list():
    def __init__(self):
        self.klist = []
    def down(self, key):
        if key not in self.klist:
            self.klist.append(key)
    def up(self, key):
        if key in self.klist:
            self.klist.remove(key)
    def pressed(self, key):
        return key in self.klist