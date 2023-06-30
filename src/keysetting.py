import pygame as pg
import util
from util import Button

norm = [['up','down','left','right','turn left','turn right','fast mode'],['alter arm','skill1','skill2','skill3','skill4','skill5','skill6']]

class KeySetting():
    def __init__(self):
        self.screen =  pg.display.get_surface()
        self.rect = self.screen.get_rect()

        self.read_config()
        self.load_buttons()

        self.c_col = 0
        self.c_row = 0

        self.running = True

        font = pg.font.SysFont('Calibri', 28)
        font = font.render('Press any key:', True, (255,255,255), (0,0,0))
        font.set_colorkey((0,0,0))
        font_rect = font.get_rect()
        wait_image = pg.Surface((self.rect.width/2, self.rect.height/2))
        wait_image.fill((99,123,45))
        font_rect.center = wait_image.get_rect().center
        wait_image.blit(font, font_rect)
        self.wait_image = wait_image

    def load_buttons(self):
        margin = 10
        width = (self.rect.width - margin)/2 - margin
        height = (self.rect.height - margin)/8 - margin

        self.buttons = []
        for col in range(len(norm)):
            col_list = []
            for row in range(len(norm[0])):
                if norm[col][row] not in self.config:
                    self.config[norm[col][row]] = None
                text = norm[col][row]
                text = ''.join((text.ljust(10, ' '),':',pg.key.name(self.config[text]).rjust(10, ' ') if self.config[text] is not None else 'None'.rjust(10, ' ')))
                col_list.append(Button(text, pg.Rect(margin + (width + margin) * col, margin + (height + margin) * row, width, height)))
            self.buttons.append(col_list)

        self.buttons[0].append(Button('Default', pg.Rect(margin + (width + margin) * 0, margin + (height + margin) * 7, width, height)))
        self.buttons[1].append(Button('OK', pg.Rect(margin + (width + margin) * 1, margin + (height + margin) * 7, width, height)))

    def draw(self):
        self.screen.fill((0,0,0))
        for col in self.buttons:
            for button in col:
                self.screen.blit(button.up_image, button.rect)
        self.screen.blit(self.buttons[self.c_col][self.c_row].down_image, self.buttons[self.c_col][self.c_row].rect)
        pg.display.update()
        
    def start(self):
        clock = pg.time.Clock()
        while self.running:
            clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        break
                    if event.key == pg.K_UP:
                        self.c_row = (self.c_row - 1) % len(self.buttons[self.c_col])
                    if event.key == pg.K_DOWN:
                        self.c_row = (self.c_row + 1) % len(self.buttons[self.c_col])
                    if event.key == pg.K_LEFT:
                        self.c_col = (self.c_col - 1) % len(self.buttons)
                        #self.c_row = 0
                    if event.key == pg.K_RIGHT:
                        self.c_col = (self.c_col + 1) % len(self.buttons)
                        #self.c_row = 0
                    if event.key == pg.K_RETURN:
                        if self.buttons[self.c_col][self.c_row].text == 'Default':
                            self.default_config()
                            self.read_config()
                            self.load_buttons()
                            self.draw()
                            #self.running = False
                            break
                        elif self.buttons[self.c_col][self.c_row].text == 'OK':
                            #self.write_config()
                            self.running = False
                            break
                        else:
                            self.screen.blit(self.wait_image, (self.rect.width/4, self.rect.height/4))
                            pg.display.update()
                            while True:
                                event = pg.event.wait()
                                if event.type == pg.KEYDOWN:
                                    if event.key == pg.K_ESCAPE:
                                        break
                                    text = norm[self.c_col][self.c_row]
                                    text = ''.join((text.ljust(10, ' '),':',pg.key.name(event.key).rjust(10, ' ') if key is not None else 'None'.rjust(10, ' ')))
                                    self.buttons[self.c_col][self.c_row] = Button(text, self.buttons[self.c_col][self.c_row].rect)
                                    self.config[norm[self.c_col][self.c_row]] = event.key
                                    self.write_config()
                                    self.draw()
                                    break
            self.draw()


    def read_config(self):
        #with open('configure/key_setting.json', 'r') as f:
        #    self.config = json.load(f)
        self.config = util.read_config('key_setting.json')
    
    def write_config(self):
        #with open('configure/key_setting.json', 'w') as f:
        #    json.dump(self.config, f, indent=4)
        util.write_config('key_setting.json', self.config)

    def default_config(self):
        #with open('configure/key_default.json', 'r') as f:
        #    self.config = json.load(f)
        #with open('configure/key_setting.json', 'w') as f:
        #    json.dump(self.config, f, indent=4)
        util.write_config('key_setting.json', util.read_config('key_default.json'))

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Key Setting')
    pg.display.set_mode((800,600))
    KeySetting().start()
    pg.quit()