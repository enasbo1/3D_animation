from collections.abc import Sequence
from random import randint

import pygame as pyg
import backwork.direction as direct


class PygIO:
    mouse = pyg.mouse

    def __init__(self):
        pyg.init()
        pyg.font.init()
        self.screen = pyg.display.set_mode()
        self.inputKeys = pyg.key.get_pressed()
        n = pyg.display.Info()
        self.width = n.current_w
        self.height = n.current_h
        self.clock = pyg.time.Clock()
        self.running = True
        self.screen_color = '#555555'
        self.draw = pyg.draw

    def prepare_update(self):
        n = pyg.display.Info()
        self.width = n.current_w
        self.height = n.current_h
        self.screen.fill(self.screen_color)

    def update(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.running = False
        if self.inputKeys[pyg.K_ESCAPE]:
            self.running = False
        pyg.display.flip()

    def getKeys(self):
        self.inputKeys = pyg.key.get_pressed()
        return self.inputKeys

    def getRandomScreenPosition(self) -> tuple[int, int]:
        return randint(-self.width//2, self.width//2), randint(-self.height//2, self.height//2)

    def end(self):
        pyg.quit()

    def draw_circle(self, x: float, y: float, r: float, color, width=0):
        self.draw.circle(self.screen, color, (x+(self.width//2), y + (self.height//2)), r)
        if width != 0:
            self.draw.circle(self.screen, '#000000', (x+(self.width//2), y + (self.height//2)), r, width)

    def draw_rect(self, x1: float, y1: float, width: float, height: float, color: str):
        self.draw.rect(self.screen, color, (x1+(self.width // 2), y1 + (self.height // 2), width, height))

    def draw_poly(self, coords: Sequence[tuple[float, float]], color: str|pyg.Color, width:int = 0):
        coords = direct.change_ref(self.width//2, self.height//2, coords)
        self.draw.polygon(self.screen, color, coords, width)

    def draw_cross(self, center: tuple[float, float], size: float, color):
        center = direct.sum_vectors((self.width//2, self.height//2), center)
        self.draw.line(self.screen, color, direct.sum_vectors(center, (-size,-size)), direct.sum_vectors(center, (size,size)), width=2)
        self.draw.line(self.screen, color, direct.sum_vectors(center, (-size,size)), direct.sum_vectors(center, (size,-size)), width=2)

    def draw_text(self, x, y, text: str, size: int, color='#000000', center=True):
        my_font = pyg.font.SysFont('Aptos', size)
        text_surface = my_font.render(text, False, color)

        # topleft, center, bottomright. Add them in param if needed
        if center:
            text_rect = text_surface.get_rect(center=(x + (self.width // 2), y + (self.height // 2)))
        else:
            text_rect = text_surface.get_rect(topleft=(x + (self.width // 2), y + (self.height // 2)))

        self.screen.blit(text_surface, text_rect)
