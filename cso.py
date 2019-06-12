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
SRD=0.2
SPC=True

FUNCTION=benchmarks.Rastrigin(2)

ITERATIONS_COUNT = 200
CATS_COUNT = 50

class CSO(object):

    #data - paczka informacji wstepnych : N (rozmiar przestrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self,iterations,cats_count,function,mr,c,smp,cdc,srd,spc):
        self.iterations=iterations
        data=cats_count,function,mr, c, smp, cdc, srd, spc
        self.swarm= cso_swarm.CatSwarm(data)

    def run_iterations(self,verbose=True):
        x_best, y_best, x_swarm, y_swarm = [[]], [[]], [[] for _ in range(self.swarm.cats_count)], [[] for _ in
        range(self.swarm.cats_count)]
        for i in range(self.iterations):
            self.swarm.cso_iteration_step()
            if(verbose):
                print('ITERATION ' + str(i))
                print(self.swarm.best.shape)
                print(self.swarm.cost_fuction(self.swarm.best))
            x_best, y_best, x_swarm, y_swarm = update_particles_positions(self.swarm, x_best, y_best, x_swarm, y_swarm)
        save_positions_to_file(x_best, y_best, x_swarm, y_swarm, self.swarm, self.iterations)
        return self.swarm.cost_fuction(self.swarm.best)

# cso=CSO(ITERATIONS_COUNT,CATS_COUNT,FUNCTION,MR, C, SMP, CDC, SRD, SPC)
# cso.run_iterations(True)

# print(FUNCTION.evaluate([[-0.01290481,-0.02309485]]))
