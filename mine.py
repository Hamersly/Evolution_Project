from kivy.app import App
from form import Form
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock


class RootScreen(ScreenManager):
    pass

class ScreenConf(Screen):
    pass

class Screen1(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.add_widget(Simulation())


class Simulation(FloatLayout):
    """Окно с инициализированным приложением"""

    def __init__(self, **kwargs):
        super(Simulation, self).__init__(**kwargs)
        Window.size = (1080, 2340)

    def inicial_form(self, **kwargs):
        """Инициализация объекта Form"""
        # self.clear_widgets()
        self.form = Form(kwargs, Window.width, Window.height)
        self.add_widget(self.form)

    def remove(self):
        """Удаление виджета"""
        self.remove_widget(self.form)

    def data_line(self):
        """Превращение словаря данных об объектах в строку"""
        slov = self.form.info
        line = tuple('#' + key + ', ' + value for key, value in slov.items())
        text = '\n'.join(line)
        return text

    def config_line(self):
        """Создание словаря конфигурации и превращение его значений в строку"""
        slov = {'Коэффициент возможности мутации, как 1/n': str(self.form.canvas_mut),
                'Коэффициент вероятности мутации клетки в хищника, как 1/n': str(self.form.pred_mut),
                'Размер клетки': str(self.form.size_cell),
                'Коэффициент пределов мутации размера клетки, как +/-': str(self.form.size_cell_mut),
                'Шаг клетки за такт': str(self.form.step_cell),
                'Коэффициент пределов мутации длины шага, как +/-': str(self.form.step_cell_mut),
                'Энергетический запас клетки': str(self.form.life_cell),
                'Коэффициент пределов мутации запаса энергии, как +/-': str(self.form.life_cell_mut),
                'Количество изначальных клеток': str(self.form.quant_cell),
                'Возможно ли деление': str(self.form.division_cell),
                'Размер энергетической ячейки': str(self.form.size_energy),
                'Количество энергетических ячеек': str(self.form.quant_energy),
                'Возможно ли создание минерала': str(self.form.create_miner)}
        line = tuple('#' + key + ': ' + value for key, value in slov.items())
        text = '\n'.join(line)
        return text

    def speed_canvas(self, value):
        """Регулировка скорости симуляции"""
        Config(value)

    def timer(self):
        return str(self.form.time)

    def start(self, speed):
        """Запуск холста и скорости вреиени"""
        Clock.schedule_interval(self.form.update, speed)
        

class LisaApp(App):
    """Запуск приложения"""

    def build(self):
        return RootScreen()


if __name__ == '__main__':
    LisaApp().run()
