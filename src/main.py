import pygame as pg
import core
import entities
import util
import keysetting

if __name__ == "__main__":
    pg.init()
    util.init()
    #screen = pg.display.set_mode((512,512), pg.SCALED)
    screen = pg.display.set_mode((1280,640), pg.SCALED)
    pg.display.set_caption('Game')
    screen.fill((255, 255, 255))

    core = core.Core(screen)
    core.load(entities.Entity(core, 0, 0, 0), [entities.Entity(core, 100, 100, 0)])

    main_page = util.Menu_Page(['start', 'alter skills', 'alter weapons', 'set keys', 'settings', 'exit'], util.get_font(28).render(util.get_word('Welcome to the game!'), True, (50,150,200)), pg.Rect(648, 0, 632, 640))
    cursor = main_page.start()
    while cursor != -1 and cursor != 5:#exit
        if cursor == 0:#start
            #core = core.Core(screen)
            #core.load(entities.Entity(core, 0, 0, 0), [entities.Entity(core, 100, 100, 0)])
            core.start()
        if cursor == 1:#alter skills
            pass
        if cursor == 2:#alter weapons
            pass
        if cursor == 3:#set keys
            keysetting.KeySetting().start()
        if cursor == 4:#settings
            pass
        cursor = main_page.start()


    

    pg.quit()