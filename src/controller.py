import pygame as pg
import visibles
import math
import random
import util
import pages.key_setting
import pages.settings
import accessories

class Controller():
    def __init__(self, original_size = (1024, 1024)):
        self.screen = pg.display.get_surface()
        if original_size is None:
            original_size = self.screen.get_size()
        self.predraw = pg.Surface(original_size)
        
        self.pressed = []

        self.camera = Camera(pg.math.Vector2(self.predraw.get_rect().center))

        self.player = None
        self.floor = None

        self.fields = pg.sprite.Group()
        self.entities = FlexibleGroup()
        self.acessories = pg.sprite.Group()
        self.interactives = pg.sprite.Group()
        self.entrances = pg.sprite.Group()

        self.stop_clocks = pg.sprite.GroupSingle()

    def load_player(self, player):
        self.player = player
        self.camera.follow = self.player
        self.camera.loc = self.player.loc.copy()
        self.camera.orientation = self.player.orientation
        self.load_directing(self.player)

    def load_floor(self, floor_image):
        if self.player is None:
            raise Exception('Please load player first')
        self.floor = visibles.Visible(self.camera, image = floor_image)
        self.boundary = pg.math.Vector2(self.floor.origional_image.get_rect().height/2,
         self.floor.origional_image.get_rect().width/2)

    def load_directing(self, entity):
        self.entities.add(entity)
        self.acessories.add(accessories.Direction_indicator(entity))
        self.acessories.add(accessories.State_bar(entity))

    def load_entity(self, entity):
        self.entities.add(entity)
        self.acessories.add(accessories.State_bar(entity))

    def start(self):
        self.keys = util.read_config('key_setting.json')

        if self.floor is None:
            raise Exception('Please load floor first')
        
        clock = pg.time.Clock()
        self.flamerate = 60
        self.blood = False
        self.state = 1
        pg.event.set_allowed([pg.QUIT, pg.KEYUP, pg.KEYDOWN])
        self.result = None
        while self.state == 1:
            clock.tick(self.flamerate)

            self.screen.fill((255, 255, 255))
            self.update()
            self.check_finish()
            pg.display.flip()
        return self.result

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

        if self.stop_clocks.sprite:
            self.stop_clocks.update()
            [e.handle_image() for e in self.entities.sprites()]
            #[e.handle_image() for e in self.fields.sprites()]
        else:
            self.entities.update()
        self.fields.update()
        self.interactives.update()
        self.entrances.update()

        self.maintain_boundaries()
        self.acessories.update()
        self.camera.update()

        self.draw()
        self.sceneupdate()

    def sceneupdate(self):
        if self.flamerate < 60:
            self.flamerate *= 2
            self.flamerate = min(self.flamerate, 60)
        self.blood = False

    def draw(self):
        self.predraw.fill((0,0,0))
        self.predraw.blit(self.floor.image, self.floor.rect)
        self.interactives.draw(self.predraw)
        self.entrances.draw(self.predraw)
        self.fields.draw(self.predraw)
        self.entities.draw(self.predraw)
        self.acessories.draw(self.predraw)
        self.screen.blit(pg.transform.scale(self.predraw, self.screen.get_rect().size), (0,0))
        if self.blood:
            blood = pg.Surface(self.screen.get_rect().size)
            blood.fill((255,0,0))
            blood.set_alpha(50)
            self.screen.blit(blood, (0,0))
        pg.display.flip()

    def keyupdate(self):
        if self.keys['turn left'] in self.pressed:
            if all([e.name != 'unmovable' for e in self.player.effects]):
                self.player.orientation += self.player.properties['turn']
        if self.keys['turn right'] in self.pressed:
            if all([e.name != 'unmovable' for e in self.player.effects]):
                self.player.orientation -= self.player.properties['turn']
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
            rect = self.screen.get_rect()
            rect.width = rect.width//2
            rect.move_ip(rect.width//2, 0)
            image = pg.transform.scale(self.predraw, self.screen.get_rect().size)
            menu = util.Button_Box(rect, button_names, image)
            message = menu.start()
            while message == 1 or message == 2:
                if message == 1:
                    pages.key_setting.Page().start()
                    self.keys = util.read_config('key_setting.json')
                if message == 2:
                    pages.settings.Page().start()
                message = menu.start()
            if message < 1:
                self.state = 1
                return
            if message == 3:
                return
            if message == 4:
                pg.quit()
                exit()
        # skills
        for i in range(1, 7):
            if key == self.keys[f'skill{i}']:
                skill = self.player.weapon.skills[i]
                skill.conduct(skill.get_direction(self.pressed, self.keys))
        # fast move
        if key == self.keys['fast mode']:
            skill = self.player.weapon.skills[0]
            skill.conduct(skill.get_direction(self.pressed, self.keys))
        elif self.keys['fast mode'] in self.pressed:
            skill = self.player.weapon.skills[0]
            skill.conduct(skill.get_direction([key], self.keys))
        # switch weapon
        if key == self.keys['alter arm']:
            self.player.switch_weapon()

        if key == self.keys['interaction']:
            for entrance in self.entrances:
                if (entrance.loc - self.player.loc).length_squared() < entrance.radius**2:
                    self.result = entrance.info
                    self.state = 5
                    return
            for interactive in self.interactives:
                if (interactive.loc - self.player.loc).length_squared() < interactive.radius**2:
                    image = pg.transform.scale(self.predraw, self.screen.get_rect().size)
                    interactive.interact(image)
                    break

    def maintain_boundaries(self):
        for entity in self.entities:
            if entity.loc.x > self.boundary.x:
                entity.loc.x = self.boundary.x
                entity.edge = True
            elif entity.loc.x < -self.boundary.x:
                entity.loc.x = -self.boundary.x
                entity.edge = True
            if entity.loc.y > self.boundary.y:
                entity.loc.y = self.boundary.y
                entity.edge = True
            elif entity.loc.y < -self.boundary.y:
                entity.loc.y = -self.boundary.y
                entity.edge = True

    def check_finish(self):
        if self.player.hp <= 0:
            self.state = 5

class Camera():
    def __init__(self, center, follow = None):
        self.loc = pg.math.Vector2(0, 0)
        self.orientation = 0
        self.follow = follow
        self.center = center
        self.shake = 0

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
        
        if self.shake:
            self.shake -= 1
            self.loc += pg.math.Vector2(random.randint(-5,5), random.randint(-5,5))

class FlexibleGroup(pg.sprite.Group):
    def draw(self, surface, bgsurf=None, special_flags=0):  
        sprites = sorted(self.sprites(), key = lambda sprite: sprite.rect.center[1])
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (spr.image, spr.rect, None, special_flags) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(
                    spr.image, spr.rect, None, special_flags
                )
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty