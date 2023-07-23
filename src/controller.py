import pygame as pg
import visibles
import math
import util
import keysetting

class Controller():
    def __init__(self, original_size = None):
        self.screen = pg.display.get_surface()
        if original_size is None:
            original_size = self.screen.get_size()
        self.predraw = pg.Surface(original_size)
        
        self.pressed = []

        self.camera = Camera(pg.math.Vector2(self.predraw.get_rect().center))

        self.player = None
        self.floor = None

        self.fields = pg.sprite.Group()
        self.entities = pg.sprite.Group()
        self.acessories = pg.sprite.Group()

    def load_player(self, player):
        self.player = player
        self.camera.follow = self.player
        self.camera.loc = self.player.loc.copy()
        self.camera.orientation = self.player.orientation
        self.entities.add(self.player)

    def load_floor(self, floor_image):
        if self.player is None:
            raise Exception('Please load player first')
        self.floor = visibles.Visible(self.camera, image = floor_image)

    def start(self):
        self.keys = util.read_config('key_setting.json')

        if self.floor is None:
            raise Exception('Please load floor first')
        
        clock = pg.time.Clock()
        self.flamerate = 60
        self.state = 1
        pg.event.set_allowed([pg.QUIT, pg.KEYUP, pg.KEYDOWN])
        while self.state == 1:
            clock.tick(self.flamerate)

            self.screen.fill((255, 255, 255))
            self.update()
            self.check_finish()
            pg.display.flip()

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
        self.floor.update()
        self.entities.update()
        self.maintain_boundaries()
        self.fields.update()
        self.acessories.update()
        self.camera.update()

        self.draw()

    def draw(self):
        self.predraw.fill((0,0,0))
        self.predraw.blit(self.floor.image, self.floor.rect)
        self.fields.draw(self.predraw)
        self.entities.draw(self.predraw)
        self.acessories.draw(self.predraw)
        self.screen.blit(pg.transform.scale(self.predraw, self.screen.get_rect().size), (0,0))
        pg.display.flip()

    def keyupdate(self):
        if self.keys['turn left'] in self.pressed:
            self.player.orientation += 3
        if self.keys['turn right'] in self.pressed:
            self.player.orientation -= 3
        if self.keys['up'] in self.pressed:
            self.player.move(0)
        if self.keys['down'] in self.pressed:
            self.player.move(180)
        if self.keys['left'] in self.pressed:
            self.player.move(90)
        if self.keys['right'] in self.pressed:
            self.player.move(-90)

    def keypress(self, key):
        if key == pg.K_ESCAPE:
            self.state = 0
            button_names = ['continue', 'set keys', 'settings', 'main page', 'exit']
            menu = util.Button_Box(self.screen.get_rect(), button_names, self.screen.copy())
            message = menu.start()
            while message == 1 or message == 2:
                if message == 1:
                    keysetting.KeySetting().start()
                    self.keys = util.read_config('key_setting.json')
                self.screen.fill((0,0,0))
                message = menu.start()
            if message < 1:
                self.state = 2
                return
            if message == 3:
                return
            if message == 4:
                pg.quit()
                exit()
        #if key == self.keys['skill1']:
        #    self.hero.skills[1].act_withkeys(self.hero, self.pressed, self.keys)
        #if key == self.keys['skill2']:
        #    self.hero.skills[2].act_withkeys(self.hero, self.pressed, self.keys)
        #if key == self.keys['skill3']:
        #    self.hero.skills[3].act_withkeys(self.hero, self.pressed, self.keys)
        #if key == self.keys['skill4']:
        #    self.hero.skills[4].act_withkeys(self.hero, self.pressed, self.keys)
        #if key == self.keys['skill5']:
        #    self.hero.skills[5].act_withkeys(self.hero, self.pressed, self.keys)
        #if key == self.keys['skill6']:
        #    self.hero.skills[6].act_withkeys(self.hero, self.pressed, self.keys)
        #fast move
        #if key == self.keys['fast mode']:
        #    self.hero.skills[0].act_withkeys(self.hero, self.pressed, self.keys)
        #elif self.keys['fast mode'] in self.pressed:
        #    self.hero.skills[0].act_withkey(self.hero, key, self.keys)

    def drawUI(self):
        head = pg.transform.scale(self.hero.ori_image,(32,32))
        self.screen.blit(head, (4,4))
        width = 8
        leftlimit = 32+8
        rightlimit = self.screen.get_width()*2//5
        point = pg.math.lerp(leftlimit, rightlimit, self.hero.health_point/self.hero.max_hp)
        margin = 8
        pg.draw.line(self.screen, (255,0,0,100), (leftlimit, margin), (point, margin), width)
        pg.draw.line(self.screen, (155,155,155,100), (point, margin), (rightlimit, margin), width)
        point = pg.math.lerp(leftlimit, rightlimit, self.hero.magis_point/self.hero.max_mp)
        margin = 20
        pg.draw.line(self.screen, (0,0,255,100), (leftlimit, margin), (point, margin), width)
        pg.draw.line(self.screen, (155,155,155,100), (point, margin), (rightlimit, margin), width)
        margin = 4
        count = 0
        for effect in self.hero.effects:
            if isinstance(effect, effects.icon):
                self.screen.blit(effect.image, (rightlimit+width+count*(32+2), margin))
                count += 1

    def maintain_boundaries(self):
        x_limit = self.floor.origional_image.get_rect().width//2
        y_limit = self.floor.origional_image.get_rect().height//2
        for entity in self.entities:
            x = pg.math.clamp(entity.loc.x, -x_limit, x_limit)
            y = pg.math.clamp(entity.loc.y, -y_limit, y_limit)
            entity.loc = pg.math.Vector2(x, y)

    def check_finish(self):
        if self.player.hp <= 0:
            self.state = 5

class Camera():
    def __init__(self, center, follow = None):
        self.loc = pg.math.Vector2(0, 0)
        self.orientation = 0
        self.follow = follow
        self.center = center

    def update(self):
        if self.follow is None:
            return

        if self.loc.distance_squared_to(self.follow.loc) < 25:
            self.loc = self.follow.loc.copy()
        else:
            self.loc = self.loc.lerp(self.follow.loc, 0.3)

        dif = self.orientation - self.follow.orientation
        if abs(dif) < 10:
            self.orientation = self.follow.orientation
        else:
            self.orientation -= dif/2
