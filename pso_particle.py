import numpy as np


class Particle(object):

    # data - paczka informacji wstepnych : N (rozmiar przezstrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self, data):
        index, N, benchmark_min, benchmark_max, cost_function, swarm = data
        self.swarm = swarm
        self.index = index
        self.cost_fuction = cost_function
        self.x, self.v = self.initialize_positions_and_velocity(N, benchmark_min, benchmark_max)
        self.p = self.x

    def initialize_positions_and_velocity(self, N, benchmark_min, benchmark_max):
        position = np.zeros(shape=(1, N))
        velocity = np.zeros(shape=(1, N))
        for i in range(N):
            position[0, i] = np.random.uniform(benchmark_min, benchmark_max, 1)[0]
            velocity[0, i] = np.random.uniform(-(benchmark_max - benchmark_min), benchmark_max - benchmark_min, 1)[0]
        return position, velocity

    def update_local_optimum(self):
        if self.cost_fuction(self.x[0]) < self.cost_fuction(self.p[0]):
            self.p = self.x

    def update_velocity(self, w, cp, cg):
        rp = np.random.uniform(0, 1, 1)[0]
        rg = np.random.uniform(0, 1, 1)[0]
        v_new = w * self.v + cp * rp * (self.p - self.x) + cg * rg * (self.swarm.g - self.x)
        self.v = v_new

    def update_position(self):
        self.x += self.v

    def __str__(self):
        return 'index: {0}, position: {1}, best: {2}'.format(self.index, self.x, self.p)
