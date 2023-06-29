import pygame as pg
import core
import entities
import effects
import skills
import math

class Core():
    def __init__(self, screen):
        self.screen = screen
        self.ori_screen = pg.Surface((screen.get_width(), screen.get_height()*3/2))
        
        self.pressed = []

        self.camera = Camera(self.ori_screen.get_rect().center)
        self.background = Background(self.camera)
        self.constants = [self.background, self.camera]
    
        self.hero = entities.Entity(self, self.camera)
        self.enemy = entities.Entity(self, self.camera)
        self.entities = pg.sprite.Group(self.hero, self.enemy)
        self.spaces = pg.sprite.Group()

        self.camera.ref = self.hero

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                self.pressed.append(event.key)
                self.keypress(event.key)
            elif event.type == pg.KEYUP:
                self.pressed.remove(event.key)
        self.keyupdate()
        self.background.update()
        self.camera.update()

        self.entities.update()
        self.spaces.update()

        #screen.blit(self.background.image, self.background.rect)
        #self.spaces.draw(screen)
        #self.entities.draw(screen)
        self.ori_screen.fill((0,0,0))
        self.ori_screen.blit(self.background.image, self.background.rect)
        self.spaces.draw(self.ori_screen)
        self.entities.draw(self.ori_screen)
        self.screen.blit(pg.transform.scale(self.ori_screen, self.screen.get_rect().size), (0,0))
        
    def keyupdate(self):
        if pg.K_LEFT in self.pressed:
            self.hero.effects.append(effects.simple_turn(self.hero, 5))
        if pg.K_RIGHT in self.pressed:
            self.hero.effects.append(effects.simple_turn(self.hero, -5))
        if pg.K_UP in self.pressed:
            self.hero.effects.append(effects.simple_forward(self.hero, 10))
        if pg.K_DOWN in self.pressed:
            self.hero.effects.append(effects.simple_forward(self.hero, -10))

    def keypress(self, key):
        if key == pg.K_SPACE:
            skills.sample_cut(self, self.hero)

class Background(entities.Visible):
    def __init__(self, camera):
        super().__init__(camera, 0, 0, 0)
        image = pg.image.load('./res/bigBackground.png')
        #image = pg.transform.scale(image,(1024,1024)).convert_alpha()
        image = pg.transform.scale(image,(1024,1024)).convert()
        #image.set_colorkey((255,255,255))
        self.ori_image = image
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.center = self.center

    def update(self):
        super().update()
        x, y, orient = self.absolute_location()
        self.rect.center = (x, y)

        #self.image = self.ori_image.copy()

        self.image = pg.transform.rotate(self.ori_image, orient)
        self.rect = self.image.get_rect(center=self.rect.center)

class Camera(pg.sprite.Sprite):
    def __init__(self, center, ref = None):
        super().__init__()
        
        #self.center = pg.display.get_surface().get_rect().center
        self.center = center
        self.ref = ref

        self.loc_x = 0
        self.loc_y = 0
        self.o = 0
        self.orient = self.o - 90

    def update(self):
        super().update()
        if self.ref is None:
            return
        dx = self.loc_x - self.ref.loc_x
        dy = self.loc_y - self.ref.loc_y
        do = self.o - self.ref.orient
        if abs(dx) < 2:
            self.loc_x = self.ref.loc_x
        else:
            self.loc_x -= dx/2

        if abs(dy) < 2:
            self.loc_y = self.ref.loc_y
        else:
            self.loc_y -= dy/2
        
        if abs(do) < 30:
            self.o = self.ref.orient
        else:
            self.o -= do/2
        self.orient = self.o - 90

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((512,512), pg.SCALED)
    screen.fill((255, 255, 255))

    core = Core(screen)
    clock = pg.time.Clock()

    going = True
    pg.event.set_allowed([pg.QUIT, pg.KEYUP, pg.KEYDOWN])
    while going:
        clock.tick(30)

        screen.fill((255, 255, 255))
        core.update()
        pg.display.flip()

    pg.quit()