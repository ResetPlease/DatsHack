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
        * `setScaler(k : float)` - устанавливает коэффициент масштабирования
        * `ScaleUp()` - мастабируется вверх в коэффициент масштабирования
        * `ScaleDown()` - мастабируется вниз в коэффициент масштабирования
        * `getMousePos() -> tuple` и `getMousePoint() -> Point` возвращают позицию мыши в соотвествующих типах
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
        self.scale_k = 1.1

        pygame.font.init() # инициализируем шрифты
        pygame.font.Font(None, 24)

        self.base_Camera = Point(0,0)
        self.Camera = Point(0,0)
        self.lastCameraPosition = Point(0,0)
        self.movable = False
        self.CAMERA_SPEED = 10

    def run(self, func = lambda x : None) -> None:
        self.__run(func)

    def CameraMove(self, dx, dy) -> None:
        self.base_Camera = self.base_Camera + (dx*self.CAMERA_SPEED,dy*self.CAMERA_SPEED)
        self.Camera = self.base_Camera*self.scale

    def setTick(self, tick : int) -> None:
        self.tick = tick

    def setCameraSpeed(self, speed : float) -> None:
        self.CAMERA_SPEED = speed

    def setScaler(self, k : float) -> None:
        self.scale_k = k
    
    def ScaleUp(self) -> None:
        self.scale *= self.scale_k
    
    def ScaleDown(self) -> None:
        self.scale /= self.scale_k

    def __run(self, func = lambda x : None) -> None:
        run = True
        while run:
            self.clock.tick(self.tick)
            self.screen.fill(self.__background_color)
            self.movable = False
            if self.lastCameraPosition != self.base_Camera:
                self.movable = True
            func(pygame.event.get())
            for i in range(len(self.data)):
                if isinstance(self.data[i], Rectangle):
                    self.__rect(self.data[i])
                elif isinstance(self.data[i], Circle):
                    self.__circle(self.data[i])
                elif isinstance(self.data[i], Triangle):
                    self.__triangle(self.data[i])
                elif isinstance(self.data[i], Text):
                    self.__text(self.data[i])
                else:
                    raise Exception(f"Wrong object i type={type(i)}")
            if self.movable:
                self.lastCameraPosition = Point(self.base_Camera)
            pygame.display.flip()
        pygame.quit

    def setBackground(self, color : Color) -> None:
        self.__background_color = color()
    
    def setObjects(self, list_of_objects : list) -> None:
        self.data = list_of_objects # ?????
    
    def getMousePosition(self) -> tuple:
        """
            Return a relative position
        """
        mouse = Point(pygame.mouse.get_pos())
        mouse = mouse*(1/self.scale)+self.base_Camera
        return mouse()

    def getMousePoint(self) -> Point:
        """
            Return a relative position(Point)
        """
        return Point(self.getMousePosition())
    
    def getAbsoluteMousePosition(self) -> tuple:
        """
            Return absolute mouse position
        """
        return pygame.mouse.get_pos()
    
    def getAbsoluteMousePoint(self) -> Point:
        """
            Return absolute mouse position(Point)
        """
        return Point(self.getAbsoluteMousePosition())

    def __rect(self, object : Rectangle) -> None:
        object.setScale(self.scale)
        if self.movable:
            dx,dy = (self.lastCameraPosition - self.base_Camera)()
            object.move(dx, dy, iscamera=True)
        pygame.draw.rect(self.screen, object.color(), object.obj)
    
    def __circle(self, object : Circle) -> None:
        object.setScale(self.scale)
        if self.movable:
            dx,dy = (self.lastCameraPosition - self.base_Camera)()
            object.move(dx, dy, iscamera=True)
        pygame.draw.circle(self.screen, object.color(), (object.x, object.y), object.r)

    def __triangle(self, object : Triangle) -> None:
        object.setScale(self.scale)
        if self.movable:
            dx,dy = (self.lastCameraPosition - self.base_Camera)()
            object.move(dx, dy, iscamera=True)
        pygame.draw.polygon(self.screen, object.color(), object.getPoints())
    
    def __text(self, object : Text) -> None:
        element = object.render()
        self.screen.blit(element, element.get_rect(center = object.point()))