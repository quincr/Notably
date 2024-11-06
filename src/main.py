import pygame as pg

display = pg.display.set_mode((800, 600))

running = True
while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False

    pg.display.flip()
    display.fill(0)
