import pygame as pg
import core
import entities


if __name__ == "__main__":
    pg.init()
    #screen = pg.display.set_mode((512,512), pg.SCALED)
    screen = pg.display.set_mode((640,640), pg.SCALED)
    screen.fill((255, 255, 255))

    core = core.Core(screen)
    core.load(entities.Entity(core, 0, 0, 0), [entities.Entity(core, 100, 100, 0)])

    running = True
    while running:
        core.start()

        clock = pg.time.Clock()
        while core.state == 3:
            clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        core.state = 1
                        break

    pg.quit()