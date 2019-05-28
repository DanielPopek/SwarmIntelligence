import numpy as np


class Bee(object):
    def __init__(self, benchmark):
        self.fitness = 0
        self.f = benchmark
        self.pos = self.f.custom_sample()


class EmployedScoutBee(Bee):
    def __init__(self, benchmark, limit=10):
        super(EmployedScoutBee, self).__init__(benchmark)
        self.limit = limit
        self.timer = self.limit

    def explore_if_needed(self):
        self.timer = self.timer - 1
        if self.timer == 0:
            self.pos = self.f.custom_sample()
            self.timer = self.limit


class OnlookerBee(Bee):
    def __init__(self, benchmark, neighbourhood=0.1):
        super(OnlookerBee, self).__init__(benchmark)
        self.employee = EmployedScoutBee
        self.neighbourhood = neighbourhood

    def fly_to_food(self, employee, random_neighbour):
        self.pos = employee.pos + self.neighbourhood * (random_neighbour.pos - employee.pos)
        self.employee = employee

    def swap_with_parent_if_needed(self):
        if self.fitness > self.employee.fitness:
            self.pos, self.employee.pos = self.employee.pos, self.pos
            self.fitness, self.employee.fitness = self.employee.fitness, self.fitness


class Hive(object):
    LIMIT = 10
    NEIGHBOURHOOD = 0.1

    def __init__(self, n, benchmark):
        self.f = benchmark
        self.best_bee_pos = [0, 0]
        self.bees_employed = []
        self.bees_onlookers = []
        self.n = n

    def update_fitness(self):
        bees = self.bees_employed + self.bees_onlookers
        bees_evaluation_values = [self.f(bee.pos) for bee in bees]
        f_min, f_max = min(bees_evaluation_values), max(bees_evaluation_values)
        for i, bee in enumerate(bees):
            bee.fitness = 1 - (bees_evaluation_values[i] - f_min) / (f_max - f_min)

    def roulette(self):
        self.update_fitness()
        fitness_values = np.array([bee.fitness for bee in self.bees_employed])
        probabilities = list(fitness_values / np.sum(fitness_values))
        employees = np.random.choice(self.bees_employed, self.n/2, p=probabilities)
        random_neighbours = np.random.choice(self.bees_employed, self.n/2)

        return employees, random_neighbours

    def update_onlookers_pos(self):
        employees, random_neighbours = self.roulette()
        for i, onlooker in self.bees_onlookers:
            onlooker.fly_to_food(employees[i], random_neighbours[i])
            onlooker.swap_with_parent_if_needed()

    def send_scouts_for_exploration(self):
        for potential_scout in self.bees_employed:
            potential_scout.explore_if_needed()
        self.update_fitness()
