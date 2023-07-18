import pygame as pg
import core
import entities
import util
import keysetting
import skills_setting
import levels

def win_page():
    screen = pg.display.get_surface()
    picture = util.load_image('basic/win_page.png', screen.get_width(), screen.get_height())
    picture.blit(util.get_font(28).render(util.get_word('You win!'), True, (150,220,160)), (20, 20))
    screen.blit(picture, (0,0))
    pg.display.update()
    pg.time.delay(1000)
    pg.event.wait()

def lose_page():
    screen = pg.display.get_surface()
    picture = util.load_image('basic/lose_page.png', screen.get_width(), screen.get_height())
    picture.blit(util.get_font(28).render(util.get_word('You lose!'), True, (0,0,50)), (20, 20))
    screen.blit(picture, (0,0))
    pg.display.update()
    pg.time.delay(1000)
    pg.event.wait()

def load_game():
    core0 = core.Core()
    levels.load_game(core0)
    if core0.state == 4:
        win_page()
    elif core0.state == 5:
        lose_page()

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
            util.loading_page()
            skills_setting.skills_setting().start()
        if cursor == 2:#alter weapons
            pass
        if cursor == 3:#set keys
            util.loading_page()
            keysetting.KeySetting().start()
        if cursor == 4:#settings
            pass
        cursor = main_page.start()
    
    pg.quit()