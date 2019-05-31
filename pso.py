import pickle

import pso_swarm
import benchmarks
import math


def update_particles_positions(swarm, x_best, y_best, x_swarm, y_swarm):
    for i, particle in enumerate(swarm.particles):
        x_swarm[i].append(particle.x[0][0])
        y_swarm[i].append(particle.x[0][1])
    x_best[0].append(swarm.g[0])
    y_best[0].append(swarm.g[1])
    return x_best, y_best, x_swarm, y_swarm


def save_positions_to_file(x_best, y_best, x_swarm, y_swarm, swarm, iterations):
    file_name = f"./tests/pso/{swarm.f.name}_{swarm.particles_count}_particles_in_" \
        f"{iterations}iterations.txt"
    with open(file_name, "wb") as fp:
        pickle.dump([x_best, y_best, x_swarm, y_swarm], fp)


W = 0.729
CP = 1.49445
CG = 1.49445

FUNCTION = benchmarks.Ackley(2)
ITERATIONS_COUNT = 200
PARTICLES_COUNT = 40


class PSO(object):

    # data - paczka informacji wstepnych : N (rozmiar przestrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self):
        data = PARTICLES_COUNT, FUNCTION
        self.swarm = pso_swarm.Swarm(data)
        self.w = W

    # po to by sprawdzić jak zmniejszanie W wpływa na zbieganie do optimum globalnego (redukowanie eksploracji)
    def inertion_update_strategy(self):
        pass

    def run_iterations(self, verbose=True):
        x_best, y_best, x_swarm, y_swarm = [[]], [[]], [[] for _ in range(self.swarm.particles_count)], [[] for _ in range(
            self.swarm.particles_count)]
        for i in range(ITERATIONS_COUNT):
            self.swarm.pso_iteration_step(self.w, CP, CG)
            self.inertion_update_strategy()
            if verbose:
                print('ITERATION ' + str(i))
                print(self.swarm)
            x_best, y_best, x_swarm, y_swarm = update_particles_positions(self.swarm, x_best, y_best, x_swarm, y_swarm)
        save_positions_to_file(x_best, y_best, x_swarm, y_swarm, self.swarm, ITERATIONS_COUNT)


pso = PSO()
pso.run_iterations()
