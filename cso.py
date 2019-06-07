import cso_swarm
import benchmarks
import pickle

def update_particles_positions(swarm, x_best, y_best, x_swarm, y_swarm):
    for i, cat in enumerate(swarm.cats):
        x_swarm[i].append(cat.x[0][0])
        y_swarm[i].append(cat.x[0][1])
    x_best[0].append(swarm.best[0][0])
    y_best[0].append(swarm.best[0][1])
    return x_best, y_best, x_swarm, y_swarm


def save_positions_to_file(x_best, y_best, x_swarm, y_swarm, swarm, iterations):
    file_name = f"./tests/cso/{swarm.f.name}_{swarm.cats_count}_cats_in_" \
        f"{iterations}iterations.txt"
    with open(file_name, "wb") as fp:
        pickle.dump([x_best, y_best, x_swarm, y_swarm], fp)

C= 1.5
MR=0.1
SMP=10
CDC=2
SRD=0.3
SPC=True

FUNCTION=benchmarks.Ackley(2)

ITERATIONS_COUNT = 350
CATS_COUNT = 20

class CSO(object):

    #data - paczka informacji wstepnych : N (rozmiar przestrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self):
        data=CATS_COUNT,FUNCTION,MR, C, SMP, CDC, SRD, SPC
        self.swarm= cso_swarm.CatSwarm(data)

    def run_iterations(self,verbose=True):
        x_best, y_best, x_swarm, y_swarm = [[]], [[]], [[] for _ in range(self.swarm.cats_count)], [[] for _ in
        range(self.swarm.cats_count)]
        for i in range(ITERATIONS_COUNT):
            self.swarm.cso_iteration_step()
            if(verbose):
                print('ITERATION '+str(i))
                print(self.swarm)
                print(self.swarm.g)
            x_best, y_best, x_swarm, y_swarm = update_particles_positions(self.swarm, x_best, y_best, x_swarm, y_swarm)
        save_positions_to_file(x_best, y_best, x_swarm, y_swarm, self.swarm, ITERATIONS_COUNT)

cso=CSO()
cso.run_iterations()


