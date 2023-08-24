import pygame as pg
import controller
import visibles
import entities
import util
import pages.key_setting
import pages.skill_setting
import pages.settings
import pages.equiptment_setting
import skills.skills

def map1(ctrler):
    entity = visibles.Entity(ctrler, pg.math.Vector2(100, 100), 0, 1, util.load_image_alpha('entities/human1.png',(64,64)))
    ctrler.load_directing(entity)
    interactive = visibles.Interactive(ctrler.camera, pg.math.Vector2(100, 100), 0, 64)
    ctrler.interactives.add(interactive)
    info = {'loc': pg.math.Vector2(0, 0), 'orientation': 0, 'map_name': 'floor/bigBackground.png', 'test': 2}
    entrance = visibles.Entrance(ctrler.camera, pg.math.Vector2(0, 0), 0, 64, info)
    ctrler.entrances.add(entrance)

def map2(ctrler):
    entity = entities.RandomWalk(ctrler, pg.math.Vector2(100, 100), 0, util.load_image_alpha('entities/human1.png',(64,64)))
    ctrler.load_directing(entity)
    info = {'loc': pg.math.Vector2(0, 0), 'orientation': 0, 'map_name': 'floor/colorful.png', 'test': 1}
    entrance = visibles.Entrance(ctrler.camera, pg.math.Vector2(0, 0), 0, 64, info)
    ctrler.entrances.add(entrance)

def load_map(info):
    ctrler = controller.Controller()
    player = entities.Player(ctrler, info['loc'], info['orientation'], util.load_image_alpha('entities/human0.png',(64,64)))
    player.skills = [skills.skills.FastMove(player)]
    ctrler.load_player(player)
    ctrler.load_floor(util.load_image(info['map_name'],(1024,1024), (0,0,0)))

    if info['test'] == 1:
        map1(ctrler)
    elif info['test'] == 2:
        map2(ctrler)

    return ctrler.start()

def load_game():
    result = {'loc': pg.math.Vector2(0, 0), 'orientation': 0, 'map_name': 'floor/bigBackground.png', 'test': 2}
    result = load_map(result)
    while result != None:
        result = load_map(result)

def get_size():
    desktop_size = pg.display.get_desktop_sizes()[0]
    unit = min(desktop_size[0]/3, desktop_size[1]/2) - 10
    return (int(unit*3), int(unit*2))

if __name__ == "__main__":
    pg.init()
    util.init()
    pg.display.set_caption('Game')
    screen = pg.display.set_mode(get_size())
    size = screen.get_size()
    
    screen.fill((255, 255, 255))

    util.show_loading_page()

    main_picture = util.load_image('basic/main_page.png', size)
    util.get_font(28).render_to(main_picture, (size[0]//2-20, 10), util.get_word('Welcome to the game!'), (250,120,120))
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
        if buttons[message] == 'settings':
            util.show_loading_page()
            pages.settings.Page().start()
        if buttons[message] == 'alter weapons':
            util.show_loading_page()
            pages.equiptment_setting.Page().start()
        message = main_page.start()
    
    pg.quit()