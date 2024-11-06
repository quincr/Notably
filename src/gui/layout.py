from __future__ import annotations

import pygame as pg

from . import DEBUG_RENDER, _getDebugColor
from .base import BaseElement
from .text import Text


class VerticalLayout(BaseElement):
    def __init__(
        self: VerticalLayout,
        position: pg.Vector2,
        size: pg.Vector2,
        scrollable: bool = False,
    ) -> None:
        self.position = position
        self.size = size

        self.elements: list[type[BaseElement]] = []

    def AddElement(self: VerticalLayout, element: type[BaseElement]) -> None:
        self.elements.append(element)

    def IsMouseHovering(self: VerticalLayout) -> bool:
        return pg.Rect(self.absolute_position, self.size).collidepoint(
            *pg.mouse.get_pos()
        )

    def Tick(self: VerticalLayout) -> None:
        is_pressing = pg.mouse.get_pressed(3)[0]
        just_pressed = pg.mouse.get_just_pressed()[0]
        is_hovering_container = self.IsMouseHovering()

        y_offset = 0

        for element in self.elements:
            element.relative_position = self.relative_position + pg.Vector2(
                element.position
            )
            element.absolute_position = (
                self.absolute_position
                + pg.Vector2(element.position)
                + pg.Vector2(0, y_offset)
            )

            element.is_hovering = is_hovering_container and element.IsMouseHovering()
            element.is_pressed = is_pressing and element.is_hovering
            element.is_just_pressed = just_pressed and element.is_hovering

            element.Tick()
            y_offset += element.GetHeight()

    def Render(self: VerticalLayout, surface: pg.Surface) -> None:
        container_surface = pg.Surface(self.size, pg.SRCALPHA)

        y_offset = 0

        for element in self.elements:
            element.relative_position.y = y_offset

            if type(element) == Text:
                element.Render(
                    container_surface, max_width=self.size[0] - element.position.x
                )
                continue

            element.Render(container_surface)
            y_offset += element.GetHeight()

        if DEBUG_RENDER:
            pg.draw.rect(
                container_surface, _getDebugColor(id(self)), ((0, 0), self.size), 1
            )

        surface.blit(container_surface, self.position)
