from __future__ import annotations
import pygame
from customtypes import Point, Color, Rectangle, Circle
from typing import Union
from copy import deepcopy

class GUI:
    """
        Даже не стоит вникать. Пример работы описан в `main.py`

        Из существенного можно выделить некоторые функции:
        
        * `setBackground(color : Color)` - устанавливает цвет для фона. По умолчанию Color.WHITE
        * `setObjects(list_of_objects : list)` - устанавливает набор объектов для отрисовки
        * `setTick(tick : int)` - устанавливает количество кадров в секунду. По умолчанию 10
    """

    def __init__(self, w : int, h : int, title = "App") -> None:
        """
            `w` - ширина окна

            `h` - длина окна

            `title` - заголовок окна
        """
        pygame.init()
        self.__background_color = Color.WHITE
        self.size = self.width, self.height =  w, h
        self.screen = pygame.display.set_mode(self.size)
        self.title = title
        pygame.display.set_caption(self.title)
        self.screen.fill(self.__background_color)
        self.data = []
        self.clock = pygame.time.Clock()
        self.tick = 10

    def run(self, func = lambda x : None) -> None:
        self.__run(func)

    def setTick(self, tick : int) -> None:
        self.tick = tick

    def __run(self, func = lambda x : None) -> None:
        run = True
        while run:
            self.clock.tick(self.tick)
            self.screen.fill(self.__background_color)
            func(pygame.event.get())
            for i in self.data:
                if isinstance(i, Rectangle):
                    self.__rect(i)
                else:
                    self.__circle(i)
            pygame.display.flip()
        pygame.quit

    def setBackground(self, color : Color) -> None:
        self.__background_color = color()
    
    def setObjects(self, list_of_objects : list) -> None:
        self.data = deepcopy(list_of_objects)
    
    def __rect(self, object : Rectangle) -> None:
        pygame.draw.rect(self.screen, object.color(), object.obj)
    
    def __circle(self, object : Circle) -> None:
        pygame.draw.circle(self.screen, object.color(), (object.x, object.y), object.r)