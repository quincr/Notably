from __future__ import annotations

import pygame as pg

class Font():
    def __init__(self: Font, path: str) -> None:
        self._font_register = {}
        self._base_path = path

    def Get(self: Font, size: int) -> pg.Font:
        if not size in self._font_register:
            self._font_register[size] = pg.font.Font(self._base_path, size)
        
        return self._font_register[size]

class Text():
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
