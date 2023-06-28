import pygame as pg
import core
import entities
import effects
import skills
import math

class Core():
    def __init__(self):
        self.pressed = []

        self.camera = Camera()
        self.background = Background(self.camera)
        self.constants = [self.background, self.camera]
    
        self.hero = entities.Entity(self.camera)
        self.enemy = entities.Entity(self.camera)
        self.entities = pg.sprite.Group(self.hero, self.enemy)
        self.spaces = pg.sprite.Group()

        self.camera.ref = self.hero

    def update(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                self.pressed.append(event.key)
            elif event.type == pg.KEYUP:
                self.pressed.remove(event.key)
        self.keyupdate()
        self.background.update()
        self.camera.update()

        self.entities.update()
        removing = []
        for entities in self.entities:
            if entities.health_point == 0:
                removing.append(entities)
        for entities in removing:
            self.entities.remove(entities)

        self.spaces.update()
        removing = []
        for space in self.spaces:
            if space.life <= 0:
                removing.append(space)
        for space in removing:
            self.spaces.remove(space)

        screen.blit(self.background.image, self.background.rect)
        self.spaces.draw(screen)
        self.entities.draw(screen)

    def keyupdate(self):
        if pg.K_LEFT in self.pressed:
            self.hero.effects.append(effects.simple_left_turn(self.hero, 5))
        if pg.K_RIGHT in self.pressed:
            self.hero.effects.append(effects.simple_right_turn(self.hero, 5))
        if pg.K_UP in self.pressed:
            self.hero.effects.append(effects.simple_forward(self.hero, 5))
        if pg.K_DOWN in self.pressed:
            self.hero.effects.append(effects.simple_forward(self.hero, -5))
        if pg.K_SPACE in self.pressed:
            skills.sample_cut(self, self.hero, self.hero.loc_x, self.hero.loc_y, self.hero.orient)



class Background(pg.sprite.Sprite):
    def __init__(self, camera):
        super().__init__()
        image = pg.image.load('./res/bigBackground.png')
        #image = pg.transform.scale(image,(1024,1024)).convert_alpha()
        image = pg.transform.scale(image,(1024,1024)).convert()
        #image.set_colorkey((255,255,255))
        self.ori_image = image
        self.image = image
        self.rect = self.image.get_rect()

        self.center = pg.display.get_surface().get_rect().center
        self.rect.center = self.center
        self.camera = camera

        self.loc_x = 0
        self.loc_y = 0
        self.orient = 0

    def update(self):
        super().update()
        camera = self.camera
        rad = math.radians(camera.orient)
        cos = math.cos(rad)
        sin = math.sin(rad)
        dx = self.loc_x - camera.loc_x
        dy = self.loc_y - camera.loc_y
        ref_x = cos*dx - sin*dy
        ref_y = sin*dx + cos*dy
        self.rect.center = (self.center[0]+ref_x, self.center[1]+ref_y)

        #self.image = self.ori_image.copy()

        ref_orient = self.orient - self.camera.orient
        self.image = pg.transform.rotate(self.ori_image, ref_orient)
        self.rect = self.image.get_rect(center=self.rect.center)

class Camera(pg.sprite.Sprite):
    def __init__(self, ref = None):
        super().__init__()
        
        self.center = pg.display.get_surface().get_rect().center
        self.ref = ref

        self.loc_x = 0
        self.loc_y = 0
        self.orient = 0

    def update(self):
        super().update()
        if self.ref is None:
            return
        dx = self.loc_x - self.ref.loc_x
        dy = self.loc_y - self.ref.loc_y
        do = self.orient - self.ref.orient
        if abs(dx) < 2:
            self.loc_x = self.ref.loc_x
        else:
            self.loc_x -= dx/2

        if abs(dy) < 2:
            self.loc_y = self.ref.loc_y
        else:
            self.loc_y -= dy/2
        
        if abs(do) < 30:
            self.orient = self.ref.orient
        else:
            self.orient -= do/2

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((512,512), pg.SCALED)
    screen.fill((255, 255, 255))

    core = Core()
    clock = pg.time.Clock()

    going = True
    pg.event.set_allowed([pg.QUIT, pg.KEYUP, pg.KEYDOWN])
    while going:
        clock.tick(30)

        screen.fill((255, 255, 255))
        core.update(screen)
        pg.display.flip()

    pg.quit()