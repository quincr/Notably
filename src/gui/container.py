from __future__ import annotations

import pygame as pg

from . import DEBUG_RENDER, _getDebugColor
from .base import BaseElement
from .text import Text


class Container(BaseElement):
    def __init__(self: Container, position: pg.Vector2, size: pg.Vector2) -> None:
        self.position = position
        self.size = size

        self.elements: list[type[BaseElement]] = []

    def AddElement(self: Container, element: type[BaseElement]) -> None:
        self.elements.append(element)

    def IsMouseHovering(self: Container) -> bool:
        return pg.Rect(self.position + self.relative_position, self.size).collidepoint(
            *pg.mouse.get_pos()
        )

    def Tick(self: Container):
        is_pressing = pg.mouse.get_pressed(3)[0]
        just_pressed = pg.mouse.get_just_pressed()[0]
        is_hovering_container = self.IsMouseHovering()

        for element in self.elements:
            element.is_hovering = is_hovering_container and element.IsMouseHovering()
            element.is_pressed = is_pressing and element.is_hovering
            element.is_just_pressed = just_pressed and element.is_hovering
            element.relative_position = self.relative_position + element.position

            element.Tick()

    def Render(self: Container, surface: pg.Surface) -> None:
        container_surface = pg.Surface(self.size, pg.SRCALPHA)

        for element in self.elements:
            if type(element) == Text:
                element.Render(
                    container_surface, max_width=self.size[0] - element.position.x
                )
                continue

            element.Render(container_surface)

        if DEBUG_RENDER:
            pg.draw.rect(
                container_surface, _getDebugColor(id(self)), ((0, 0), self.size), 1
            )

        surface.blit(container_surface, self.position)
