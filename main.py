from gui import GUI
from customtypes import Color, Rectangle, Circle, Triangle, Point
import pygame
from Interface import Interface
import config

manager = Interface(config.TOKEN)
manager.Register("GET_SOMETHING_DATA", "http://www.google.com", "GET")


#инициализация класса отрисовщика
gui = GUI(700,700, "DatsHack")

GOLUBENKIY = (0, 191, 255)

#установка цвета фона (ОПЦИОНАЛЬНО)
gui.setBackground(Color(GOLUBENKIY))

#создаем объекты для отрисовки
r = Rectangle(50,50, 50,50, Color(Color.RED))
c = Circle(10, 10, 20, Color(Color.BLUE))
t = Triangle(Point(300,300), Point(400,400), Point(300,400), color=Color(Color.RED))

#главная функция где должна происходить отрисовка
@gui.run
def main(events):
    c.move(1,1) # двигает объект(в данном случае круг) на dx и dy соответственно
    for event in events: # обработка событий
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos) # печатаем координату нажатия мыши
            if r.collidepoint(pos[0], pos[1]): # если нажали на прямоугольник `r`
                print("COLLIDE RECT")
            if c.collidepoint(pos[0], pos[1]): # если нажали на круг `c`
                print("COLLIDE CIRCLE")
            if t.collidepoint(pos[0], pos[1]): # если нажали на треугольник
                print("COLLIDE TRIANGLE")
        elif event.type == pygame.KEYDOWN: # обработка событий нажатия на клавиши
            """
                Подробнее обо всех событиях клавиатуры на
                http://surl.li/sduil            
                PS. Надеюсь эта сокращенная ссылка все еще будет работать
            """
            if event.key == pygame.K_LEFT: # двигаемся на правую и левую стрелочки
                r.move(-10,0)
            elif event.key == pygame.K_RIGHT:
                r.move(10,0)
            elif event.key == pygame.K_DOWN:
                t.rotate(-15)                # теперь треугольник можно поворачивать
            elif event.key == pygame.K_ESCAPE:
                exit()

    gui.setObjects([r,c, t]) # самое главное - отрисовка всех элементов(кругов и прямоугольников)

"""
    Закрыть отрисовщик на Escape
"""

if __name__ == "__main__":
    main()