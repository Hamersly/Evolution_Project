from kivy.uix.widget import Widget
from objects import *


class Form(Widget):
    """Класс создания холста"""

    def __init__(self, config, x, y):
        super().__init__()
        self.division_cell = config['division_cell']
        self.create_miner = config['create_miner']
        self.canvas_mut = config['canvas_mut']
        self.pred_mut = config['pred_mut']
        self.size_cell_mut = config['size_cell_mut']
        self.step_cell_mut = config['step_cell_mut']
        self.life_cell_mut = config['life_cell_mut']
        self.size_energy = config['size_energy']
        self.quant_energy = int(config['quant_energy'])
        self.quant_cell = config['quant_cell']
        self.life_cell = config['life_cell']
        self.step_cell = config['step_cell']
        self.size_cell = config['size_cell']
        self.info = {}
        self.window_size_x = x
        self.window_size_y = int(y / 2)
        self.speed_anim = config['speed_anim']
        self.predators = []
        self.cells = []
        self.minerals = []
        self.energy_list = []
        self.time = 0
        self.n = 0
        self.quantity_cell(self.quant_cell)
        self.quantity_energy(self.quant_energy)

    def create_mineral(self, obj):
        """Создание минерала"""
        if self.create_miner == True:
            for i in range(1):
                i = Mineral(obj.size, obj.pos, obj.size[0])
                self.add_widget(i)
                self.minerals.append(i)

    def division_predator(self, predator):
        """Деление хищников"""
        if self.config.DIVISION_PREDATOR == True:
            for i in range(1):
                i = Predator(predator.pos[0], predator.pos[1], self.speed_anim)
                self.add_widget(i)
                self.predators.append(i)

    def division_cells(self, cell):
        """Деление леток"""
        if self.division_cell == True:
            mutation_now = self.mutation_in_predator(self.pred_mut)
            if mutation_now == False or len(self.cells) == 1:
                self.mutation_protocol(Cell, cell, self.cells)
            else:
                self.mutation_protocol(Predator, cell, self.predators)

    def mutation_protocol(self, class_obj, cell, list, name=None):
        """Сценарий мутации"""
        for i in range(1):
            i = class_obj(cell.pos[0], cell.pos[1],self.speed_anim, self.mutation_probability(self.canvas_mut, 
                self.life_cell_mut, cell.first_life),
                self.mutation_probability(self.canvas_mut, 
                    self.step_cell_mut, cell.step),
                self.mutation_probability(self.canvas_mut, self.size_cell_mut, cell.size[0]))
            self.add_widget(i)
            list.append(i)
            self.n += 1
            self.info[str(self.n)] = 'Энергия:' + str(i.life) +\
                  ', Шаг: ' + str(i.step) +\
                  ', Размер: ' + str(i.size[0]) +\
                  ' (Кол-во клеток: ' + str(len(self.cells)) +\
                  ', Кол-во хищников: ' + str(len(self.predators)) + ')'

    def mutation_probability(self, canvas_mut, index, value):
        """Вероятность мутации"""
        prob = random.randint(0, canvas_mut)
        prob2 = random.randint(0, canvas_mut)
        if prob == prob2:
            mutation = random.randint(value - index, value + index)
        else:
            mutation = value
        return mutation

    def mutation_in_predator(self, pred_mut):
        """Вероятность мутации в хищника"""
        prob = random.randint(0, pred_mut)
        prob2 = random.randint(0, pred_mut)
        if prob == prob2:
            mutation = True
        else:
            mutation = False
        return mutation


    def quantity_cell(self, quan):
        """Количество создаваемых изначально клеток"""
        for i in range(quan):
            i = Cell(self.window_size_x / 2, self.window_size_y + self.window_size_y / 2, self.speed_anim, self.life_cell, self.step_cell, self.size_cell)
            self.add_widget(i)
            self.cells.append(i)
            self.n += 1
            self.info[str(self.n)] = 'Энергия:' + str(i.life) +\
                  ', Шаг: ' + str(i.step) +\
                  ', Размер: ' + str(i.size[0]) +\
                  ' (Кол-во клеток: ' + str(len(self.cells)) +\
                  ', Кол-во хищников: ' + str(len(self.predators)) + ')'


    def positions_objects(self, object_list):
        """Позиция живых объектов на холсте"""
        for obj in object_list.copy():
            obj.position(self.window_size_x,
                             self.window_size_y)
            if obj.life == 0:
                self.remove_widget(obj)
                self.create_mineral(obj)
                object_list.remove(obj)

    def quantity_energy(self, quan):
        """Количество создаваемых изначально ячеек энергии"""
        for i in range(quan):
            i = Energy(size=(self.size_energy, self.size_energy), pos=(random.randint(
            self.size_cell, self.window_size_x - self.size_cell), random.randint(self.window_size_y + self.size_cell, self.window_size_y * 2 - self.size_cell)))
            self.add_widget(i)
            self.energy_list.append(i)

    def cell_mineral_position(self):
        """Поведение клетки при встрече с минералом"""
        for cell in self.cells.copy():
            for mineral in self.minerals.copy():
                if abs(cell.pos[0] - mineral.pos[0]) <= cell.size[0] / 2 and abs(cell.pos[1] - mineral.pos[1]) <= cell.size[0] / 2:
                    cell.pos = mineral.pos
                    cell.life += mineral.life
                    self.remove_widget(mineral)
                    self.minerals.remove(mineral)

    def cell_box_position(self):
        """Поведение клетки при встече с энерг-ой ячейкой"""
        for cell in self.cells.copy():
            for box in self.energy_list.copy():
                if abs(cell.pos[0] - box.pos[0]) <= cell.size[0] / 2 and abs(cell.pos[1] - box.pos[1]) <= cell.size[0] / 2:
                    cell.pos = box.pos
                    self.division_cells(cell)
                    self.remove_widget(box)
                    self.energy_list.remove(box)
                    self.quantity_energy(1)

    def predator_cell_position(self):
        """Поведение хищника при встрече с клеткой"""
        for predator in self.predators.copy():
            for cell in self.cells.copy():
                if abs(predator.pos[0] - cell.pos[0]) <= predator.size[0] / 2 and abs(predator.pos[1] - cell.pos[1]) <= predator.size[0] / 2:
                    predator.pos = cell.pos
                    self.remove_widget(cell)
                    self.cells.remove(cell)
                    predator.life += cell.life

    def update(self, _):
        """Обновление содержимого холста"""
        if len(self.cells) > 100 or len(self.cells) == 0 and len(self.predators) == 0:
            return
        self.positions_objects(self.cells)
        self.positions_objects(self.predators)
        self.cell_mineral_position()
        self.cell_box_position()
        self.predator_cell_position()
        self.time += 1
        
