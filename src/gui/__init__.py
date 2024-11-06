import time

import pygame as pg

DEBUG_RENDER = True  # os.getenv('NGUI_DO_DEBUG_RENDER') != None


def _getDebugColor(v: int) -> pg.Color:
    v += int(time.time())

    return pg.Color(
        (v * 2632.255) % 255, (v * (3727 + v % 17)) % 255, (v * (1822 * (v % 6))) % 255
    )


from .box import Box
from .container import Container
from .font import Font
from .layout import VerticalLayout
from .manager import Manager
from .pressable import Pressable
from .text import Text
