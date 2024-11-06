from __future__ import annotations

import pygame as pg

from . import DEBUG_RENDER, _getDebugColor
from .base import BaseElement
from .font import Font


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
