import pygame as pg
import entities
import effects
import skills
import math
import util

class Core():
    def __init__(self, screen):
        self.state = 0 # 0:unprepared, 1:prepared, 2:running, 3:paused, 4:finished
        self.screen = screen
        self.ori_screen = pg.Surface((screen.get_width(), int(screen.get_height()*2)))
        
        self.pressed = []

        self.camera = Camera(self.ori_screen.get_rect().center)
        self.background = Background(self.camera)
    
        #self.hero = entities.Entity(self, self.camera)
        #self.enemy = entities.Entity(self, self.camera)
        self.entities = None
        self.spaces = pg.sprite.Group()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key not in self.pressed:
                    self.pressed.append(event.key)
                self.keypress(event.key)
            elif event.type == pg.KEYUP:
                if event.key in self.pressed:
                    self.pressed.remove(event.key)
        self.keyupdate()
        self.background.update()
        self.camera.update()

        self.entities.update()
        self.solve_collision()
        self.spaces.update()

        #screen.blit(self.background.image, self.background.rect)
        #self.spaces.draw(screen)
        #self.entities.draw(screen)
        self.ori_screen.fill((0,0,0))
        self.ori_screen.blit(self.background.image, self.background.rect)
        self.spaces.draw(self.ori_screen)
        self.entities.draw(self.ori_screen)
        self.screen.blit(pg.transform.scale(self.ori_screen, self.screen.get_rect().size), (0,0))
        self.drawUI()
        
    def keyupdate(self):
        if self.keys['turn left'] in self.pressed:
            self.hero.effects.append(effects.simple_turn(self.hero, 5))
        if self.keys['turn right'] in self.pressed:
            self.hero.effects.append(effects.simple_turn(self.hero, -5))
        if self.keys['up'] in self.pressed:
            self.hero.effects.append(effects.simple_forward(self.hero, 10))
        if self.keys['down'] in self.pressed:
            self.hero.effects.append(effects.simple_forward(self.hero, -10))

    def keypress(self, key):
        if key == pg.K_ESCAPE:
            self.state = 3
        if key == self.keys['skill1']:
            skills.sample_cut(self.hero)
        if key == self.keys['skill2']:
            skills.fire_boll(self.hero)

    def drawUI(self):
        head = pg.transform.scale(self.hero.ori_image,(32,32))
        head = pg.transform.rotate(head, 90)
        self.screen.blit(head, (4,4))
        width = 8
        leftlimit = 32+8
        rightlimit = self.screen.get_width()*2//5
        point = pg.math.lerp(leftlimit, rightlimit, self.hero.health_point//self.hero.max_hp)
        margin = 8
        pg.draw.line(self.screen, (255,0,0,100), (leftlimit, margin), (point, margin), width)
        pg.draw.line(self.screen, (155,155,155,100), (point, margin), (rightlimit, margin), width)
        point = pg.math.lerp(leftlimit, rightlimit, self.hero.magis_point//self.hero.max_mp)
        margin = 20
        pg.draw.line(self.screen, (0,0,255,100), (leftlimit, margin), (point, margin), width)
        pg.draw.line(self.screen, (155,155,155,100), (point, margin), (rightlimit, margin), width)
        margin = 4
        count = 0
        for effect in self.hero.effects:
            if isinstance(effect, effects.icon):
                self.screen.blit(effect.image, (rightlimit+width+count*32, margin))
                count += 1

    def solve_collision(self):
        x_limit = self.background.ori_image.get_rect().width//2
        y_limit = self.background.ori_image.get_rect().height//2
        for entity in self.entities:
            x, y, orient = entity.loc_x, entity.loc_y, entity.orient
            if x < -x_limit:
                entity.loc_x = -x_limit
            elif x > x_limit:
                entity.loc_x = x_limit
            if y < -y_limit:
                entity.loc_y = -y_limit
            elif y > y_limit:
                entity.loc_y = y_limit

        for i in range(len(self.entities)):
            for j in range(i+1, len(self.entities)):
                entity1 = self.entities.sprites()[i]
                entity2 = self.entities.sprites()[j]
                overlap = entity1.size + entity2.size - math.sqrt((entity1.loc_x - entity2.loc_x)**2 + (entity1.loc_y - entity2.loc_y)**2)
                if overlap > 0:
                    if entity1.loc_x == entity2.loc_x:
                        entity1.loc_x += overlap/2
                        entity2.loc_x -= overlap/2
                    else:
                        angle = math.atan((entity1.loc_y - entity2.loc_y)/(entity1.loc_x - entity2.loc_x))
                        entity1.loc_x += overlap/2 * math.cos(angle)
                        entity2.loc_x -= overlap/2 * math.cos(angle)
                        entity1.loc_y += overlap/2 * math.sin(angle)
                        entity2.loc_y -= overlap/2 * math.sin(angle)

    def load(self, hero, enemys):
        self.hero = hero
        self.entities = pg.sprite.Group(self.hero, *enemys)
        self.camera.ref = self.hero
        self.state = 1

    def start(self):
        self.keys = util.read_config('key_setting.json')

        if self.state == 0:
            raise Exception('Core not prepared')
        
        clock = pg.time.Clock()

        self.state = 2
        pg.event.set_allowed([pg.QUIT, pg.KEYUP, pg.KEYDOWN])
        while self.state == 2:
            clock.tick(30)

            self.screen.fill((255, 255, 255))
            self.update()
            pg.display.flip()

            if self.hero.health_point <= 0:
                self.state = 4

class Background(entities.Visible):
    def __init__(self, camera):
        super().__init__(camera, 0, 0, 0)
        #image = pg.image.load('./res/bigBackground.png')
        #image = pg.transform.scale(image,(1024,1024)).convert_alpha()
        image = util.load_image('floor/bigBackground.png', 1024, 1024)
        if image is None:
            image = pg.Surface((1024,1024))
        #image = pg.transform.scale(image,(1024,1024)).convert()
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
    #screen = pg.display.set_mode((512,512), pg.SCALED)
    screen = pg.display.set_mode((768,768), pg.SCALED)
    screen.fill((255, 255, 255))

    core = Core(screen)
    core.load(entities.Entity(core, 0, 0, 0), [entities.Entity(core, 100, 100, 0)])
    core.start()

    pg.quit()