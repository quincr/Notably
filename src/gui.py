from __future__ import annotations

import os
import time
from typing import Any, Callable

import pygame as pg

DEBUG_RENDER = True  # os.getenv('NGUI_DO_DEBUG_RENDER') != None


def _getDebugColor(v: int) -> pg.Color:
    v += int(time.time())

    return pg.Color(
        (v * 2632.255) % 255, (v * (3727 + v % 17)) % 255, (v * (1822 * (v % 6))) % 255
    )


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

            element.Tick()

    def Render(self: Manager) -> None:
        window_surface = pg.display.get_surface()

        for element in self.elements:
            element.Render(window_surface)


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


class Font:
    def __init__(self: Font, path: str) -> None:
        self._font_register = {}
        self._base_path = path

    def Get(self: Font, size: int) -> pg.Font:
        if not size in self._font_register:
            self._font_register[size] = pg.font.Font(self._base_path, size)

        return self._font_register[size]


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

    def IsMouseHovering(self: Container) -> bool:
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


class Text(BaseElement):
    def __init__(
        self: Text,
        font: Font,
        text: str,
        size: int,
        color: pg.Color,
        position: pg.Vector2,
    ) -> None:
        self.position = pg.Vector2(position)
        self.size = size
        self.text = text
        self.color = color
        self.font = font

        self.Update()

    def Update(self: Text) -> None:
        self._renderred = self.font.Get(self.size).render(self.text, True, self.color)

    def Render(self: Text, surface: pg.Surface, max_width: int = -1) -> None:
        if max_width <= 0:
            surface.blit(self._renderred, self.position)

            if DEBUG_RENDER:
                pg.draw.rect(
                    surface,
                    _getDebugColor(id(self)),
                    (self.position, self._renderred.get_size()),
                    1,
                )
            return

        if self._renderred.get_width() <= max_width:
            surface.blit(self._renderred, self.position)

            if DEBUG_RENDER:
                pg.draw.rect(
                    surface,
                    _getDebugColor(id(self)),
                    (self.position, self._renderred.get_size()),
                    1,
                )
            return

        remaining_words = self.text.split(" ")

        current_line = ""
        current_y = 0
        current_width = 0

        while len(remaining_words) > 0:
            this_word = remaining_words[0]

            renderred_word = self.font.Get(self.size).render(
                this_word + ("" if current_line == "" else " "), True, self.color
            )
            if renderred_word.get_width() + current_width < max_width:
                current_width += renderred_word.get_width()
                current_line += ("" if current_line == "" else " ") + this_word

                remaining_words.remove(this_word)
            else:
                if current_width == 0:
                    return

                surface.blit(
                    self.font.Get(self.size).render(current_line, True, self.color),
                    self.position + pg.Vector2(0, current_y),
                )

                current_y += (
                    self.font.Get(self.size)
                    .render(current_line, True, self.color)
                    .get_height()
                )
                current_line = ""
                current_width = 0

        last_line = self.font.Get(self.size).render(current_line, True, self.color)

        surface.blit(
            last_line,
            self.position + pg.Vector2(0, current_y),
        )

        if DEBUG_RENDER:
            pg.draw.rect(
                surface,
                _getDebugColor(id(self)),
                (self.position, (max_width, current_y + last_line.get_height())),
                1,
            )


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

    def GetWidth(self: Box) -> int:
        return self.size.x

    def GetHeight(self: Box) -> int:
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
