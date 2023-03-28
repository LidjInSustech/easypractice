import pygame as pg
import entity
import movable
import key_list
import background
import enemy
import cevent
import attack

if __name__ == "__main__":
    pg.init()
    cevent.init()
    screen = pg.display.set_mode((512,512), pg.SCALED)
    screen.fill((255, 255, 255))

    keys = key_list.Key_list()
    hero = movable.Movable()
    enemy = enemy.Enemy(hero)
    group = pg.sprite.Group(background.Background(hero), hero, enemy)
    keydict = {pg.K_i:hero.move_forward, pg.K_k:hero.move_backward,
        pg.K_u:hero.turn_left, pg.K_o:hero.turn_right}

    clock = pg.time.Clock()

    pg.event.set_allowed(
        [pg.QUIT, pg.KEYUP, pg.KEYDOWN, cevent.ATTACK, cevent.LIFE_BORN, cevent.LIFE_KILL])
    going = True
    while going:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN:
                keys.down(event.__dict__['key'])
                if event.__dict__['key'] == pg.K_a:
                    attack.generate(hero, hero)
            elif event.type == pg.KEYUP:
                keys.up(event.__dict__['key'])
            elif event.type == cevent.LIFE_KILL:
                group.remove(event.__dict__['sprite'])
            elif event.type == cevent.LIFE_BORN:
                group.add(event.__dict__['sprite'])
            elif event.type == cevent.ATTACK:
                event.__dict__['target'].damage(event.__dict__['damage'])
        for key in keys.klist:
            if key in keydict.keys():
                keydict[key]()
        group.update()
        screen.fill((255, 255, 255))
        group.draw(screen)
        pg.display.flip()

    pg.quit()