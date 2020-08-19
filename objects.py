from kivy.uix.widget import Widget
import random
from kivy.animation import Animation


class Objects(Widget):
    """Класс, описывающий свойства и функции объекта"""

    def __init__(self, x, y, speed_anim, life, step, size):
        super().__init__()
        self.size = size, size
        self.step = step
        self.life = life
        self.first_life = life
        self.pos = (x, y)
        self.speed_anim = speed_anim

    def position(self, window_size_x, window_size_y):
        """Параметры движения клетки по холсту"""

        pos = (0,0)
        while pos[0] <= 0 or pos[1] <= 0 or pos[0] >= window_size_x - self.size[0] or pos[1] >= window_size_x - self.size[0]:
            pos = (self.pos[0] + random.randint(-self.step, self.step),
                        self.pos[1] + random.randint(-self.step, self.step))

        self.animacia(pos)
        self.life -= 1


    def animacia(self, pos):
        self.anim = Animation(
            pos=pos, d=self.speed_anim, t='in_quad')
        self.anim.start(self)


class Cell(Objects):
    """Класс, описывающий свойства и функции объекта Клетка"""

    def position(self, window_size_x, window_size_y):
        super(Cell, self).position(window_size_x, window_size_y)

    def animacia(self, pos):
        super(Cell, self).animacia(pos)


class Predator(Objects):
    """Класс, описывающий свойства и функции объекта Хищник"""

    def position(self, window_size_x, window_size_y):
        super(Predator, self).position(window_size_x, window_size_y)

    def animacia(self, pos):
        super(Predator, self).animacia(pos)


class Food(Widget):
    """Базовый класс для энергетических объектов"""

    def __init__(self, size=None, pos=None, life=None):
        super().__init__()
        self.size = size
        self.pos = pos
        self.life = life


class Mineral(Food):
    """Класс, описывающий свойства и функции объекта Минерал"""
    pass


class Energy(Food):
    """Класс, описывающий свойства и функции объекта Энергия"""
    pass
