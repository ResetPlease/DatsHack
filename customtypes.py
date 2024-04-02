from __future__ import annotations
from typing import Any, Union
from copy import deepcopy
from pygame import Rect
from math import sin, cos, pi, acos

class Point:
    """
        На всякий случай. Может когда-нибудь пригодится.
    """
    def __init__(self, x : Union[int, float, Point, tuple], y  = 0.0) -> None:
        if isinstance(x, Point):
            self.x, self.y = x()
        elif isinstance(x, tuple) or isinstance(x, list):
            self.x, self.y = x
        else:
            self.x = x
            self.y = y

    def __call__(self) -> tuple:
        return (self.x, self.y)
    
    def copy(self) -> Point:
        return Point(self())

    def list(self) -> list:
        return list(self())

    def __str__(self) -> str:
        return f"Point{self()}"

    def __add__(self, rhs : Union[Point, float, int, tuple, list]) -> Point:
        if isinstance(rhs, Point):
            return Point(self.x+rhs.x, self.y+rhs.y)
        elif isinstance(rhs, int) or isinstance(rhs, float):
            return self + Point(rhs,rhs)
        elif isinstance(rhs, tuple) or isinstance(rhs, list):
            return self + Point(rhs)

    def __neg__(self) -> Point:    
        return Point(-self.x, -self.y)
    
    def __sub__(self, rhs : Union[Point, float, int]) -> Point:
        return self + (-rhs)
    
    def __mul__(self, rhs : Union[float, int, list, tuple]) -> Point:
        if isinstance(rhs, int) or isinstance(rhs, float):
            return Point(self.x*rhs, self.y*rhs)
        elif isinstance(rhs, list) or isinstance(rhs, tuple):
            rhs = list(rhs)
            if(len(rhs) > 2 or len(rhs) < 1):
                raise Exception("Вектор должен содержать n элементов, 1 <= n <= 2")
            result = [self.x, self.y]
            for i in range(len(rhs)):
                result[i] *= rhs[i]
            return Point(result)
        else:
            raise Exception(f"Unknowk type of rhs -> {type(rhs)}")

    def Abs(self, xc : float = 0.0, yc : float = 0.0) -> float:
        return ((self.x-xc)**2 + (self.y-yc)**2)**0.5
    
    @staticmethod
    def Scalar(a : Point, b : Point) -> float:
        return a.x*b.x + a.y*b.y

    @staticmethod
    def Distance(a : Point, b : Point) -> float:
        return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5
    
    @staticmethod
    def Manhattan(a : Point, b : Point) -> float:
        result = a-b
        return abs(result.x) + abs(result.y)
    


class Color:
    """
        Этот класс чисто для удобства (если конечно удобно будет)

        Извлечь список со значениями просто:

        obj = Color((1,2,3))

        obj() # получаем список со значениями rbg
        
        или 

        obj.tuple() # вернет кортеж с rgb
    """
    
    """
        тут просто константы некоторых цветов

        Использовать так:
            black = Color(Color.BLACK)
    """
    max_color = 256
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GRAY =  (128,128,128)
    RED =   (255,0,0)
    GREEN = (0,255,0)
    BLUE =  (0,0,255)

    def __init__(self, colors : Union[tuple, list, Color]) -> None:
        if isinstance(colors, Color):
            self.colors = deepcopy(colors.colors)
        else:
            self.colors = list(colors)

    def __call__(self) -> list:
        return self.colors

    def copy(self) -> list:
        return deepcopy(self.colors)

    def tuple(self) -> tuple:
        return tuple(self())

    def __add__(self, rhs : Union[list, tuple, Color]) -> Color:
        rhs = Color(rhs)
        return Color([(rhs()[i] + self()[i])%self.max_color for i in range(3)])

    def __neg__(self) -> Color:
        return Color([-i for i in self()])
    
    def __sub__(self, rhs : Union[list, tuple, Color]) -> Color:
        return self + (-rhs)
    
    def __mul__(self, rhs : Union[int,float]) -> Color:
        return Color([int(i*rhs) for i in self()])
    
    def __str__(self):
        return f"Color{self()}"


class Circle:
    """
        Класс круга, т.к в pygame нет Circle. Добавил обработку коллизий.


        * `move` изменяет координаты круга
        * `collidepoint` проверяет коллизию для круга и точки
    """
    def __init__(self, x:int, y : int, r : int, color = Color(Color.BLACK)) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.color = color
    
    def move(self, dx : int, dy : int) -> None:
        self.x += dx
        self.y += dy

    def collidepoint(self, x : float, y : float) -> bool:
        if (self.x-x)**2 + (self.y-y)**2 <= self.r**2:
            return True
        return False

class Rectangle:
    """
        Класс-обертка для стандартного pygame.Rect. Нужен чисто для однородности поступающий данных в GUI.


        * `move` изменяет координаты прямоугольника
        * `collidepoint` проверяет коллизию для прямоугольника и точки
    """
    def __init__(self, x : int, y : int, w : int, h : int, color = Color(Color.BLACK)) -> None:
        self.obj = Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
    
    def move(self, dx : int, dy : int) -> None:
        self.x += dx
        self.y += dy
        self.obj = Rect(self.x, self.y, self.w, self.h)
    
    def collidepoint(self, x : float, y:float) -> int:
        return self.obj.collidepoint(x,y)

class Triangle:
    """
        Так же обертка для простого треугольника.
        Нет проверки на дурака, так что пж треугольник нормальный на вход.
    """
    def __init__(self, p1 : Point, p2 : Point, p3 : Point, color : Color = Color(Color.BLACK)) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.color = color
    
    def move(self, dx : float, dy : float) -> None:
        self.p1 = self.p1 + (dx,dy)
        self.p2 = self.p2 + (dx,dy)
        self.p3 = self.p3 + (dx,dy)
    
    def __rotate(self,p : Point, angle : float) -> Point:
        result = Point(0,0)
        result.x = p.x*cos(angle) - p.y*sin(angle)
        result.y = p.x*sin(angle) + p.y*cos(angle)
        return result

    def rotate(self, angle : float) -> None:
        angle = pi/180.0*angle 
        center = Point( (self.p1.x + self.p2.x + self.p3.x)/3.0, (self.p1.y + self.p2.y + self.p3.y)/3.0 )
        self.p1 = self.__rotate(self.p1 - center, angle) + center
        self.p2 = self.__rotate(self.p2 - center, angle) + center
        self.p3 = self.__rotate(self.p3 - center, angle) + center

    def getPoints(self) -> tuple[Point]:
        return (self.p1(), self.p2(), self.p3())

    def __sign(self,p1 : Point, p2 : Point, p3 : Point) -> float:
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    def collidepoint(self, x, y) -> bool:
        pt = Point(x,y)
        has_neg, has_pos = False, False
        d1 = self.__sign(pt, self.p1, self.p2)
        d2 = self.__sign(pt, self.p2, self.p3)
        d3 = self.__sign(pt, self.p3, self.p1)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

        

if __name__ == "__main__":
    
    #Colors
    black = Color(Color.BLACK)
    gray = Color(Color.GRAY)
    white = Color(Color.WHITE)
    negative = Color([-1,-2,-3])
    simple_color = Color((1,2,3))
    print(gray*3.2 - white)
    print(gray.tuple())
    print(simple_color)

    #Points
    first = Point(1,2)
    second = Point(3,4)
    copy_first = Point(first)
    copy_first_2 = first.copy()

    print(first, copy_first, copy_first_2)

    print(first, "-", second, "=", first - second)
    print(first, "+", second, "=", first + second)
    print(first, "*", 2.0, "=", first * 2)
    print(first, "*", -2.0, "=", first * -2.0)
    print(f"Distance({first}, {second}) = {Point.Distance(first, second)}")
    print(f"Manhattan({first}, {second}) = {Point.Manhattan(first, second)}")
