from __future__ import annotations

import pygame as pg

from .base import BaseElement


class Manager:
    def __init__(self: Manager) -> None:
        self.elements: list[BaseElement] = []

    def AddElement(self: Manager, element: type[BaseElement]) -> None:
        self.elements.append(element)

    def Tick(self: Manager) -> None:
        is_pressing = pg.mouse.get_pressed(3)[0]
        just_pressed = pg.mouse.get_just_pressed()[0]

        for element in self.elements:
            element.is_hovering = element.IsMouseHovering()
            element.is_pressed = is_pressing and element.is_hovering
            element.is_just_pressed = just_pressed and element.is_hovering

            element.absolute_position = element.position
            element.relative_position = element.position.copy()

            element.Tick()

    def Render(self: Manager) -> None:
        window_surface = pg.display.get_surface()

        for element in self.elements:
            element.Render(window_surface)
