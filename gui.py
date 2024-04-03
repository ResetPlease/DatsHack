from __future__ import annotations
import pygame
from customtypes import *
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
        self.data = [] # лист с объектами
        self.clock = pygame.time.Clock()
        self.tick = 10 # FPS

        self.scale = 1.0 # для масштабирования

        pygame.font.init() # инициализируем шрифты
        pygame.font.Font(None, 24)

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
            for i in range(len(self.data)):
                if isinstance(self.data[i], Rectangle):
                    self.__rect(self.data[i])
                elif isinstance(self.data[i], Circle):
                    self.__circle(self.data[i])
                elif isinstance(self.data[i], Triangle):
                    self.__triangle(self.data[i])
                elif isinstance(self.data[i], Line):
                    self.__line(self.data[i])
                elif isinstance(self.data[i], Text):
                    self.__text(self.data[i])
                else:
                    raise Exception(f"Wrong object i type={type(i)}")
            pygame.display.flip()
        pygame.quit

    def setBackground(self, color : Color) -> None:
        self.__background_color = color()
    
    def setObjects(self, list_of_objects : list) -> None:
        self.data = list_of_objects # ?????
    
    def getMousePos(self) -> tuple:
        return pygame.mouse.get_pos()
    
    def getMousePoint(self) -> Point:
        return Point(self.getMousePos())

    def __rect(self, object : Rectangle) -> None:
        object.setScale(self.scale)
        pygame.draw.rect(self.screen, object.color(), object.obj)
    
    def __circle(self, object : Circle) -> None:
        object.setScale(self.scale)
        pygame.draw.circle(self.screen, object.color(), (object.x, object.y), object.r)

    def __triangle(self, object : Triangle) -> None:
        object.setScale(self.scale)
        pygame.draw.polygon(self.screen, object.color(), object.getPoints())
    
    def __text(self, object : Text) -> None:
        element = object.render()
        self.screen.blit(element, element.get_rect(center = object.point()))
    
    def __line(self, object : Line) -> None:
        if( object.is_smooth ):
            pygame.draw.aaline(self.screen, object.color(), object.p1(), object.p2())
        else:
            pygame.draw.line(self.screen, object.color(), object.p1(), object.p2(), object.width)