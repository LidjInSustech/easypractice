import pygame as pg
import controller
import visibles
import util
import pages.key_setting
import pages.skill_setting
import skills.skills

def load_game():
    ctrler = controller.Controller()
    player = visibles.Movable(ctrler, pg.math.Vector2(-100,0), 0, 1, util.load_image_alpha('entities/human0.png',(64,64)))
    player.skills = [skills.skills.FastMove(player)]
    ctrler.load_player(player)
    ctrler.load_floor(util.load_image('floor/bigBackground.png',(1024,1024), (0,0,0)))
    entity = visibles.Movable(ctrler, pg.math.Vector2(100, 0), 0, 2, util.load_image_alpha('entities/human1.png',(64,64)))
    ctrler.load_entity(entity)
    ctrler.start()

if __name__ == "__main__":
    pg.init()
    util.init()
    pg.display.set_caption('Game')
    screen = pg.display.set_mode()
    size = screen.get_size()
    
    screen.fill((255, 255, 255))

    util.show_loading_page()

    main_picture = util.load_image('basic/main_page.png', size)
    util.get_font(28).render_to(main_picture, (size[0]//2-20, 10), util.get_word('Welcome to the game!'), (50,220,220))
    buttons = ['start', 'alter skills', 'alter weapons', 'set keys', 'settings', 'exit']
    main_page = util.Button_Box(pg.Rect(size[0]/12,size[1]/12,size[0]/3,size[1]*0.9), buttons, main_picture)
    message = main_page.start()
    while message != -1 and buttons[message] != 'exit':
        if buttons[message] == 'start':
            util.show_loading_page()
            load_game()
        if buttons[message] == 'set keys':
            util.show_loading_page()
            pages.key_setting.Page().start()
        if buttons[message] == 'alter skills':
            util.show_loading_page()
            pages.skill_setting.Page().start()
        message = main_page.start()
    
    pg.quit()