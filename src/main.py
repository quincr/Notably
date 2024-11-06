import pygame as pg

pg.init()

from gui import Font, Text

display = pg.display.set_mode((800, 600))

font = Font('./fonts/Garet-Book.ttf')
text = Text(font, 'This is test text.', 24, (255, 255, 255), pg.Vector2(5, 5))

running = True
while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
    
    text.Render(display)

    pg.display.flip()
    display.fill(0)
