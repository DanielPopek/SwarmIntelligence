import pickle

import pso_swarm
import benchmarks
import time
import math


def update_particles_positions(swarm, x_best, y_best, x_swarm, y_swarm):
    for i, particle in enumerate(swarm.particles):
        x_swarm[i].append(particle.x[0][0])
        y_swarm[i].append(particle.x[0][1])
    x_best[0].append(swarm.best[0])
    y_best[0].append(swarm.best[1])
    return x_best, y_best, x_swarm, y_swarm


def save_positions_to_file(x_best, y_best, x_swarm, y_swarm, swarm, iterations):
    file_name = f"./tests/pso/{swarm.f.name}_{swarm.particles_count}_particles_in_" \
        f"{iterations}iterations.txt"
    with open(file_name, "wb") as fp:
        pickle.dump([x_best, y_best, x_swarm, y_swarm], fp)


W = 0.1
CP = 1.2
CG = 1.5

FUNCTION = benchmarks.Rastrigin(2)
ITERATIONS_COUNT = 100
PARTICLES_COUNT = 250


class PSO(object):

    # data - paczka informacji wstepnych : N (rozmiar przestrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self,particles_count,iter,function,w,cp,cg):
        data = particles_count, function
        self.swarm = pso_swarm.Swarm(data)
        self.iter=iter
        self.w = w
        self.cp=cp
        self.cg=cg

    # po to by sprawdzić jak zmniejszanie W wpływa na zbieganie do optimum globalnego (redukowanie eksploracji)
    def inertion_update_strategy(self):
        pass

    def run_iterations(self, verbose=True):
        x_best, y_best, x_swarm, y_swarm = [[]], [[]], [[] for _ in range(self.swarm.particles_count)], [[] for _ in range(
            self.swarm.particles_count)]
        for i in range(self.iter):
            self.swarm.pso_iteration_step(self.w, self.cp, self.cg)
            self.inertion_update_strategy()
            if verbose:
                print('ITERATION ' + str(i))
                # print(self.swarm)
                print(self.swarm.cost_fuction(self.swarm.best))
            # x_best, y_best, x_swarm, y_swarm = update_particles_positions(self.swarm, x_best, y_best, x_swarm, y_swarm)
        # save_positions_to_file(x_best, y_best, x_swarm, y_swarm, self.swarm, ITERATIONS_COUNT)
        return self.swarm.cost_fuction(self.swarm.best)

start=time.time()
pso = PSO(PARTICLES_COUNT,ITERATIONS_COUNT,FUNCTION,W,CP,CG)
pso.run_iterations(True)
end=time.time()
print(end-start)

