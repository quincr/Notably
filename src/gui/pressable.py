from __future__ import annotations

from typing import Any, Callable

import pygame as pg

from . import DEBUG_RENDER, _getDebugColor
from .base import BaseElement


class Pressable(BaseElement):
    def __init__(
        self: Pressable,
        position: pg.Vector2,
        size: pg.Vector2,
        passive_color: pg.Color,
        hover_color: pg.Color,
        pressed_color: pg.Color,
        event: Callable,
        event_args: tuple[Any] = (),
    ) -> None:
        self.position = position
        self.size = pg.Vector2(size)

        self.passive_color = passive_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color

        self.event = event
        self.event_args = event_args

    def IsMouseHovering(self: Pressable) -> bool:
        return pg.Rect(self.absolute_position, self.size).collidepoint(
            *pg.mouse.get_pos()
        )

    def Tick(self: Pressable) -> None:
        if self.is_just_pressed:
            self.event(self, *self.event_args)

    def GetWidth(self: Pressable) -> int:
        return self.size.x

    def GetHeight(self: Pressable) -> int:
        return self.size.y

    def Render(self: Pressable, surface: pg.Surface) -> None:
        _color = self.passive_color
        if self.is_hovering:
            if self.is_pressed:
                _color = self.pressed_color
            else:
                _color = self.hover_color

        pg.draw.rect(
            surface, _color, (self.position + self.relative_position, self.size)
        )

        if DEBUG_RENDER:
            pg.draw.rect(
                surface,
                _getDebugColor(id(self)),
                (self.position + self.relative_position, self.size),
                1,
            )
