from __future__ import annotations

import pygame as pg


class Font:
    def __init__(self: Font, path: str) -> None:
        self._font_register = {}
        self._base_path = path

    def Get(self: Font, size: int) -> pg.Font:
        if not size in self._font_register:
            self._font_register[size] = pg.font.Font(self._base_path, size)

        return self._font_register[size]
