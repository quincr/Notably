import pygame as pg

pg.init()

from gui import Manager, Font, Text, Box, Pressable

display = pg.display.set_mode((800, 600))

manager = Manager()

def TestPressEvent(pressable: Pressable, test_arg_1: int, test_arg_2: str) -> None:
    print("Pressable field has been pressed.", test_arg_1, test_arg_2)

font = Font('./assets/fonts/Garet-Book.ttf')
text = Text(font, 'This is test text.', 24, (255, 255, 255), pg.Vector2(5, 5))
box = Box((50, 50), (255, 0, 127), (50, 50))
pressable = Pressable((50, 200), (50, 25), (128, 0, 0), (0, 128, 0), (0, 0, 128), TestPressEvent, (1, 'test_string_arg'))

manager.AddElement(text)
manager.AddElement(box)
manager.AddElement(pressable)

running = True
while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
    
    manager.Tick()
    manager.Render()

    #if not box.IsMouseHovering():
    #    box.Render(display)

    pg.display.flip()
    display.fill(0)
