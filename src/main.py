import pygame as pg

pg.init()

from gui import Font, Text, Box

display = pg.display.set_mode((800, 600))

font = Font('./assets/fonts/Garet-Book.ttf')
text = Text(font, 'This is test text.', 24, (255, 255, 255), pg.Vector2(5, 5))
box = Box((50, 50), (255, 0, 127), (50, 50))

running = True
while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
    
    text.Render(display)

    if not box.IsMouseHovering():
        box.Render(display)

    pg.display.flip()
    display.fill(0)
