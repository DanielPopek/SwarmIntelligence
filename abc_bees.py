import numpy as np
import random


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
        self.dim = self.f.dim

    def fly_to_food_simply(self, employee, random_neighbour):
        self.pos = employee.pos + self.neighbourhood * (random_neighbour.pos - employee.pos)
        self.employee = employee

    def fly_to_food_randomly_by_neighbour(self, employee, random_neighbour):
        phi = np.random.uniform(low=-self.neighbourhood, high=self.neighbourhood, size=self.dim)
        self.pos = employee.pos + phi * (random_neighbour.pos - employee.pos)
        self.employee = employee

    def fly_to_food_uniformly_by_neighbour(self, employee, random_neighbour):
        phi = np.random.uniform(low=-self.neighbourhood, high=self.neighbourhood, size=self.dim)
        dist = np.linalg.norm(random_neighbour.pos - employee.pos)
        self.pos = employee.pos + phi * dist
        self.employee = employee

    def fly_to_food_uniformly_by_neighbourhood(self, employee, random_neighbour):  # not working good
        phi = np.random.uniform(low=-self.neighbourhood, high=self.neighbourhood, size=self.dim)
        self.pos = employee.pos + phi
        self.employee = employee

    def fly_to_food_choosing_random_dimensions(self, employee, random_neighbour):
        no_of_dimensions = random.randint(1, self.dim)
        dimensions_to_change = np.random.choice(list(range(0, self.dim)), no_of_dimensions)
        for d in range(self.dim):
            self.pos[d] = employee.pos[d]
            if d in dimensions_to_change:
                self.pos[d] += self.neighbourhood * (random_neighbour.pos[d] - employee.pos[d]) \
                               * (1 if random.randint(0, 1) == 0 else -1)
        self.employee = employee

    def swap_with_parent_if_needed(self):
        if self.fitness > self.employee.fitness:
            # print(f'  SWAP onlooker with its employee')
            self.pos, self.employee.pos = self.employee.pos, self.pos
            self.fitness, self.employee.fitness = self.employee.fitness, self.fitness
            self.employee.timer = self.employee.limit


class Hive(object):
    LIMIT = 40
    NEIGHBOURHOOD = 0.5

    def __init__(self, n_empl, n_onlook, benchmark):
        self.f = benchmark
        self.bees_employed = [EmployedScoutBee(benchmark, self.LIMIT) for _ in range(n_empl)]
        self.bees_onlookers = [OnlookerBee(benchmark, self.NEIGHBOURHOOD) for _ in range(n_onlook)]
        self.best_bee_pos = self.bees_employed[0].pos  # initialization of best bee position - just random bee
        self.n_empl = n_empl
        self.n_onlook = n_onlook

    def update_best_bee_position(self, bees_evaluation_values, all_bees_positions):
        best_bee_index = np.argmin(bees_evaluation_values)
        if self.f.evaluate(all_bees_positions[best_bee_index]) < self.f.evaluate(self.best_bee_pos):  # minimum
            self.best_bee_pos = all_bees_positions[best_bee_index]

    def update_fitness(self, bees):
        all_bees_positions = [bee.pos for bee in self.bees_employed] + [bee.pos for bee in self.bees_onlookers]
        all_bees_evaluation_values = [self.f.evaluate(bee) for bee in all_bees_positions]
        f_min, f_max = min(all_bees_evaluation_values), max(all_bees_evaluation_values)
        self.update_best_bee_position(all_bees_evaluation_values, all_bees_positions)

        bees_evaluation_values = [self.f.evaluate(bee.pos) for bee in bees]
        for i, bee in enumerate(bees):
            bee.fitness = 1 - (bees_evaluation_values[i] - f_min) / (f_max - f_min)

    def roulette(self):
        self.update_fitness(self.bees_employed)
        fitness_values = np.array([bee.fitness for bee in self.bees_employed])
        probabilities = list(fitness_values / np.sum(fitness_values))
        employees = np.random.choice(self.bees_employed, self.n_onlook, p=probabilities)
        random_neighbours = np.random.choice(self.bees_employed, self.n_onlook)
        return employees, random_neighbours

    def update_onlookers_pos(self):
        employees, random_neighbours = self.roulette()
        for i, onlooker in enumerate(self.bees_onlookers):
            onlooker.fly_to_food_randomly_by_neighbour(employees[i], random_neighbours[i])

        self.update_fitness(self.bees_onlookers)
        for i, onlooker in enumerate(self.bees_onlookers):
            onlooker.swap_with_parent_if_needed()

    def send_scouts_for_exploration_if_needed(self):
        for potential_scout in self.bees_employed:
            potential_scout.explore_if_needed()
        self.update_fitness(self.bees_employed)
