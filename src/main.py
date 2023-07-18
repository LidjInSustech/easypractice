import pygame as pg
import core
import entities
import util
import keysetting
import skills

def win_page():
    screen = pg.display.get_surface()
    picture = util.load_image('basic/win_page.png', screen.get_width(), screen.get_height())
    picture.blit(util.get_font(28).render(util.get_word('You win!'), True, (150,220,160)), (20, 20))
    screen.blit(picture, (0,0))
    pg.display.update()
    pg.time.delay(500)
    pg.event.wait()

def lose_page():
    screen = pg.display.get_surface()
    picture = util.load_image('basic/lose_page.png', screen.get_width(), screen.get_height())
    picture.blit(util.get_font(28).render(util.get_word('You lose!'), True, (150,220,160)), (20, 20))
    screen.blit(picture, (0,0))
    pg.display.update()
    pg.time.delay(500)
    pg.event.wait()

def load_game():
    core0 = core.Core()
    hero = entities.Prepared_entity(core0, [skills.fast_move(), skills.slow_cut(), skills.magic_sperm(), skills.basic(), skills.basic(), skills.basic(), skills.basic()], picture=util.load_image_alpha('entities/human0.png', 64, 64))
    hero.party = 1
    enemy = entities.Entity(core0, 100, 100, 0, picture=util.load_image_alpha('entities/human1.png', 64, 64))
    enemy.party = 2
    core0.load(hero, [enemy])
    core0.start()

    if core0.state == 4:
        win_page()

if __name__ == "__main__":
    size = (960, 640)#3:2
    pg.init()
    util.init()

    screen = pg.display.set_mode(size, pg.SCALED)
    #screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    #size = screen.get_size()
    pg.display.set_caption('Game')
    screen.fill((255, 255, 255))

    #core = core.Core(screen)
    #core.load(entities.Entity(core, 0, 0, 0), [entities.Entity(core, 100, 100, 0)])
    util.loading_page()

    main_picture = util.load_image('basic/main_page.png', size[0], size[1])
    main_picture.blit(util.get_font(28).render(util.get_word('Welcome to the game!'), True, (50,220,160)), (size[0]//2-20, 10))
    main_page = util.Button_Box(pg.Rect(0,0,size[0]//2,size[1]),['start', 'alter skills', 'alter weapons', 'set keys', 'settings', 'exit'], main_picture)
    cursor = main_page.start()
    while cursor != -1 and cursor != 5:#exit
        if cursor == 0:#start
            util.loading_page()
            load_game()
        if cursor == 1:#alter skills
            pass
        if cursor == 2:#alter weapons
            pass
        if cursor == 3:#set keys
            util.loading_page()
            keysetting.KeySetting().start()
        if cursor == 4:#settings
            pass
        cursor = main_page.start()
    
    pg.quit()