from gui import GUI
from customtypes import *
import pygame
from Interface import Interface
import config

manager = Interface(config.TOKEN)
manager.Register("GET_SOMETHING_DATA", "http://www.google.com", "GET")

# инициализация класса отрисовщика
gui = GUI(700, 700, "DatsHack")
gui.setScaler(1.1) # коэффициент масштабирования
gui.setBackground(Color(Color.WHITE))
gui.setCameraSpeed(20) # Скорость движения камеры

# создаем объекты для отрисовки
r = Rectangle(50, 50, 50, 50, Color(Color.RED))
c = Circle(10, 10, 20, Color(Color.BLUE))
t = Triangle(Point(300,300), Point(400,400), Point(300,400), color=Color(Color.RED))
testRect = Rectangle(600,600,200,200, Color(Color.MAGENTA))
SPEED = 10
    # UP = [0, -1]
    # DOWN = [0, 1]
    # LEFT = [-1, 0]
    # RIGHT = [1, 0]
vector = Vector.ZERO


"""
    Теперь можно масштабировать с помощью колесика мыши.
    Теперь можно двигать камерой(WASD) и смотреть что там "в отрицательных координатах"
"""


# Text
MousePosition = Text("Click Please", Point(200,gui.height-50), smooth=True, size=36, color = Color("#808000"))
StacicText = Text("Hello World!", Point(gui.width//2,gui.height//2), smooth=True, size=72)
ScaleText = Text(f"Scale: {gui.scale}", Point(200, gui.height-20), Color(Color.RED), size=36, smooth=True)


SECRET_OBJECT = Rectangle(2000, 2000, 300, 300, Color(Color.MAROON))
SECRET_OBJECT2 = Rectangle(-300,-300,100,100, Color(Color.BLUE))

# главная функция где должна происходить отрисовка
@gui.run
def main(events):
    global vector
    c.move(1, 1)  # двигает объект(в данном случае круг) на dx и dy соответственно
    for event in events:  # обработка событий
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == MOUSE.LEFT:
                pos = gui.getMousePoint()
                MousePosition.setText(str(pos))
                print(pos)  # печатаем координату нажатия мыши
                if r.collidepoint(pos.x, pos.y):  # если нажали на прямоугольник `r`
                    print("COLLIDE RECT")
                if c.collidepoint(pos.x, pos.y):  # если нажали на круг `c`
                    print("COLLIDE CIRCLE")
                if t.collidepoint(pos.x, pos.y): # если нажали на треугольник
                    print("COLLIDE TRIANGLE")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE.SCROLL_UP:  # Прокрутка вверх
                gui.ScaleUp()
            elif event.button == MOUSE.SCROLL_DOWN:  # Прокрутка вниз
                gui.ScaleDown()
            ScaleText.setText(f"Scale: {gui.scale}")
        elif event.type == pygame.KEYDOWN: # обработка событий нажатия на клавиши
            """
                Подробнее обо всех событиях клавиатуры на
                http://surl.li/sduil            
                PS. Надеюсь эта сокращенная ссылка все еще будет работать
            """
            if event.key == pygame.K_LEFT:  # двигаемся на правую и левую стрелочки
                vector += Vector.LEFT
            elif event.key == pygame.K_RIGHT:
                vector += Vector.RIGHT
            elif event.key == pygame.K_UP:
                vector += Vector.UP
            elif event.key == pygame.K_DOWN:
                vector += Vector.DOWN
                t.rotate(-15)                # теперь треугольник можно поворачивать
            elif event.key == pygame.K_ESCAPE:
                exit()
            
            #Движение камеры бляяя
            elif event.key == pygame.K_a:
                gui.CameraMove(-1,0)
            elif(event.key == pygame.K_d):
                gui.CameraMove(1,0)
            elif event.key == pygame.K_s:
                gui.CameraMove(0,1)
            elif event.key == pygame.K_w:
                gui.CameraMove(0,-1)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:  # двигаемся на правую и левую стрелочки
                vector -= Vector.LEFT
            elif event.key == pygame.K_RIGHT:
                vector -= Vector.RIGHT
            elif event.key == pygame.K_UP:
                vector -= Vector.UP
            elif event.key == pygame.K_DOWN:
                vector -= Vector.DOWN

    r.move((vector * SPEED).x, (vector * SPEED).y)
    data = [r,c, t, MousePosition, StacicText, testRect, ScaleText, SECRET_OBJECT, SECRET_OBJECT2]
    gui.setObjects(data) # самое главное - отрисовка всех элементов
"""
    Закрыть отрисовщик на Escape
"""

if __name__ == "__main__":
    main()

