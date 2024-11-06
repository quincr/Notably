import pygame as pg

pg.init()

from gui import Box, Container, Font, Manager, Pressable, Text

display = pg.display.set_mode((800, 600))

manager = Manager()


def TestPressEvent(pressable: Pressable, test_arg_1: int, test_arg_2: str) -> None:
    print("Pressable field has been pressed.", test_arg_1, test_arg_2)


def TestPressContainerEvent(pressable: Pressable) -> None:
    print("Container Pressable field has been pressed.")


font = Font("./assets/fonts/Garet-Book.ttf")
text = Text(font, "This is test text.", 24, (255, 255, 255), pg.Vector2(5, 5))
box = Box((50, 50), (255, 0, 127), (50, 50))
pressable = Pressable(
    (50, 200),
    (50, 25),
    (128, 0, 0),
    (0, 128, 0),
    (0, 0, 128),
    TestPressEvent,
    (1, "test_string_arg"),
)

container = Container((150, 150), (100, 100))
container_text = Text(
    font, "This text is in the container", 16, (255, 255, 255), (2, 2)
)
container_pressable = Pressable(
    pg.Vector2(5, 90),
    pg.Vector2(25, 25),
    (128, 0, 128),
    (128, 128, 0),
    (0, 128, 128),
    TestPressContainerEvent,
)
container.AddElement(container_text)
container.AddElement(container_pressable)

manager.AddElement(text)
manager.AddElement(box)
manager.AddElement(pressable)

manager.AddElement(container)

running = True
while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False

    manager.Tick()
    manager.Render()

    pg.display.flip()
    display.fill(0)
