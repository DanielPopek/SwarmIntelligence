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
            # print(f'  SCOUT bee went exploring from position {self.pos}')
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
            # print(f'  SWAP onlooker with its employee')
            self.pos, self.employee.pos = self.employee.pos, self.pos
            self.fitness, self.employee.fitness = self.employee.fitness, self.fitness
            self.employee.timer = self.employee.limit


class Hive(object):
    LIMIT = 20
    NEIGHBOURHOOD = 0.05

    def __init__(self, n, benchmark):
        self.f = benchmark
        self.bees_employed = [EmployedScoutBee(benchmark, self.LIMIT) for _ in range(int(n/2))]
        self.bees_onlookers = [OnlookerBee(benchmark, self.NEIGHBOURHOOD) for _ in range(int(n/2))]
        self.best_bee_pos = self.bees_employed[0].pos  # initialization of best bee position - just random bee
        self.n = n

    def update_best_bee_position(self, bees_evaluation_values):
        best_bee_index = np.argmin(bees_evaluation_values)
        all_bees_positions = [bee.pos for bee in self.bees_employed] + [bee.pos for bee in self.bees_onlookers]
        if self.f.evaluate(all_bees_positions[best_bee_index]) < self.f.evaluate(self.best_bee_pos):  # minimum
            self.best_bee_pos = all_bees_positions[best_bee_index]

    def update_fitness(self, bees):
        all_bees_evaluation_values = [self.f.evaluate(bee.pos) for bee in self.bees_employed] + \
                                     [self.f.evaluate(bee.pos) for bee in self.bees_onlookers]
        f_min, f_max = min(all_bees_evaluation_values), max(all_bees_evaluation_values)
        self.update_best_bee_position(all_bees_evaluation_values)

        bees_evaluation_values = [self.f.evaluate(bee.pos) for bee in bees]
        for i, bee in enumerate(bees):
            bee.fitness = 1 - (bees_evaluation_values[i] - f_min) / (f_max - f_min)

    def roulette(self):
        self.update_fitness(self.bees_employed)
        fitness_values = np.array([bee.fitness for bee in self.bees_employed])
        probabilities = list(fitness_values / np.sum(fitness_values))
        employees = np.random.choice(self.bees_employed, int(self.n/2), p=probabilities)
        random_neighbours = np.random.choice(self.bees_employed, int(self.n/2))
        return employees, random_neighbours

    def update_onlookers_pos(self):
        employees, random_neighbours = self.roulette()
        for i, onlooker in enumerate(self.bees_onlookers):
            onlooker.fly_to_food(employees[i], random_neighbours[i])

        self.update_fitness(self.bees_onlookers)
        for i, onlooker in enumerate(self.bees_onlookers):
            onlooker.swap_with_parent_if_needed()

    def send_scouts_for_exploration_if_needed(self):
        for potential_scout in self.bees_employed:
            potential_scout.explore_if_needed()
        self.update_fitness(self.bees_employed)
