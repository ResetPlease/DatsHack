from __future__ import annotations
from typing import Any, Union
from copy import deepcopy



# class Point:


class Color:
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



if __name__ == "__main__":
    black = Color(Color.BLACK)
    gray = Color(Color.GRAY)
    white = Color(Color.WHITE)
    negative = Color([-1,-2,-3])
    print(gray*3.2 - white)
    print(gray.tuple())