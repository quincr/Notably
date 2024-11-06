from __future__ import annotations

import pygame as pg

from . import DEBUG_RENDER, _getDebugColor
from .base import BaseElement


class Box(BaseElement):
    def __init__(
        self: Box, position: pg.Vector2, color: pg.Color, size: pg.Vector2
    ) -> None:
        self.position = position
        self.color = color
        self.size = pg.Vector2(size)

    def IsMouseHovering(self: Box) -> bool:
        return pg.Rect(self.absolute_position, self.size).collidepoint(
            *pg.mouse.get_pos()
        )

    def GetWidth(self: Box) -> int:
        return self.size.x

    def GetHeight(self: Box) -> int:
        return self.size.y

    def Render(self: Box, surface: pg.Surface) -> None:
        pg.draw.rect(
            surface, self.color, (self.position + self.relative_position, self.size)
        )

        if DEBUG_RENDER:
            pg.draw.rect(
                surface,
                _getDebugColor(id(self)),
                (self.position + self.relative_position, self.size),
                1,
            )
