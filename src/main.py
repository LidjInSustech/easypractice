import pygame as pg
import core
import entities
import util
import keysetting

class main_page():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.rect = self.screen.get_rect()
        picture = pg.Surface((self.rect.width/2, self.rect.height))
        picture.fill((255, 255, 255))
        picture.blit(util.get_font(28).render(util.get_word('Welcome to the game!'), True, (0,0,0)), (20, 20))
        self.beginning = picture
        self.curser = 0
        self.load_buttons()
        

    def draw(self):
        self.screen.fill((255, 255, 255))
        for button in self.buttons:
            self.screen.blit(button.up_image, button.rect)
        self.screen.blit(self.buttons[self.curser].down_image, self.buttons[self.curser].rect)
        self.screen.blit(self.beginning, (self.rect.width/2, 0))
        pg.display.update()

    def load_buttons(self):
        buttons = ['start', 'alter skills', 'alter weapons', 'set keys', 'exit']
        margin = 10
        width = (self.rect.width - margin)/2 - margin
        height = (self.rect.height - margin)/len(buttons) - margin

        self.buttons = []
        for row in range(len(buttons)):
            self.buttons.append(util.Button(buttons[row], pg.Rect(margin, margin + (height + margin) * row, width, height)))

    def start(self):
        self.running = True
        clock = pg.time.Clock()
        while self.running:
            clock.tick(60)
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    return 'exit'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        return 'exit'
                    if event.key == pg.K_DOWN:
                        self.curser = (self.curser + 1) % len(self.buttons)
                    if event.key == pg.K_UP:
                        self.curser = (self.curser - 1) % len(self.buttons)
                    if event.key == pg.K_RETURN:
                        if self.curser == 0:
                            self.running = False
                            return 'start'
                        if self.curser == 1:
                            self.running = False
                            return 'alter skills'
                        if self.curser == 2:
                            self.running = False
                            return 'alter weapons'
                        if self.curser == 3:
                            self.running = False
                            return 'set keys'
                        if self.curser == 4:
                            self.running = False
                            return 'exit'

if __name__ == "__main__":
    pg.init()
    util.init()
    #screen = pg.display.set_mode((512,512), pg.SCALED)
    screen = pg.display.set_mode((1280,640), pg.SCALED)
    pg.display.set_caption('Game')
    screen.fill((255, 255, 255))

    core = core.Core(screen)
    core.load(entities.Entity(core, 0, 0, 0), [entities.Entity(core, 100, 100, 0)])

    main_page = main_page()
    massage = main_page.start()
    while massage != 'exit':
        if massage == 'start':
            #core = core.Core(screen)
            #core.load(entities.Entity(core, 0, 0, 0), [entities.Entity(core, 100, 100, 0)])
            core.start()
        if massage == 'alter skills':
            pass
        if massage == 'alter weapons':
            pass
        if massage == 'set keys':
            keysetting.KeySetting().start()
        massage = main_page.start()


    

    pg.quit()