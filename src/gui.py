from __future__ import annotations

import pygame as pg
from typing import Any, Callable

class Manager():
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

            element.Tick()

    def Render(self: Manager) -> None:
        window_surface = pg.display.get_surface()

        for element in self.elements:
            element.Render(window_surface)

class BaseElement():
    is_hovering: bool = False
    is_pressed: bool = False
    is_just_pressed: bool = False

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

class Font():
    def __init__(self: Font, path: str) -> None:
        self._font_register = {}
        self._base_path = path

    def Get(self: Font, size: int) -> pg.Font:
        if not size in self._font_register:
            self._font_register[size] = pg.font.Font(self._base_path, size)
        
        return self._font_register[size]

class Text(BaseElement):
    def __init__(self: Text, font: Font, text: str, size: int, color: pg.Color, position: pg.Vector2) -> None:
        self.position = position
        self.size = size
        self.text = text
        self.color = color
        self.font = font

        self.Update()
    
    def Update(self: Text) -> None:
        self._renderred = self.font.Get(self.size).render(self.text, True, self.color)
    
    def Render(self: Text, surface: pg.Surface) -> None:
        surface.blit(self._renderred, self.position)

class Box(BaseElement):
    def __init__(self: Box, position: pg.Vector2, color: pg.Color, size: pg.Vector2) -> None:
        self.position = position
        self.color = color
        self.size = size

    def IsMouseHovering(self: Box) -> bool:
        return pg.Rect(self.position, self.size).collidepoint(*pg.mouse.get_pos())

    def Render(self: Box, surface: pg.Surface) -> None:
        pg.draw.rect(surface, self.color, (self.position, self.size))

class Pressable(BaseElement):
    def __init__(self: Pressable, position: pg.Vector2, size: pg.Vector2, passive_color: pg.Color, hover_color: pg.Color, pressed_color: pg.Color, event: Callable, event_args: tuple[Any] = ()) -> None:
        self.position = position
        self.size = size

        self.passive_color = passive_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color

        self.event = event
        self.event_args = event_args
    
    def IsMouseHovering(self: Pressable) -> bool:
        return pg.Rect(self.position, self.size).collidepoint(*pg.mouse.get_pos())

    def Tick(self: Pressable) -> None:
        if self.is_just_pressed:
            self.event(self, *self.event_args)

    def Render(self: Pressable, surface: pg.Surface) -> None:
        _color = self.passive_color
        if self.is_hovering:
            if self.is_pressed:
                _color = self.pressed_color
            else:
                _color = self.hover_color

        pg.draw.rect(surface, _color, (self.position, self.size))