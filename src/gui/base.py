from __future__ import annotations

import pygame as pg


class BaseElement:
    position: pg.Vector2 = pg.Vector2(0, 0)

    is_hovering: bool = False
    is_pressed: bool = False
    is_just_pressed: bool = False

    relative_position: pg.Vector2 = pg.Vector2(0, 0)
    absolute_position: pg.Vector2 = pg.Vector2(0, 0)

    def __init__(self: BaseElement) -> None:
        pass

    def Update(self: BaseElement) -> None:
        return

    def IsMouseHovering(self: BaseElement) -> bool:
        return False

    def Tick(self: BaseElement) -> None:
        pass

    def Render(self: BaseElement, surface: pg.Surface) -> None:
        pass

    def GetHeight(self: BaseElement) -> int:
        # Required!

        raise NotImplementedError()

    def GetWidth(self: BaseElement) -> int:
        # Required!

        raise NotImplementedError()
