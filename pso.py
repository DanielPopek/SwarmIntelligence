import pso_swarm
import benchmarks

W = 0.729
CP = 1.49445
CG = 1.49445

FUNCTION=benchmarks.SampleFunction(2)
ITERATIONS_COUNT = 150
PARTICLES_COUNT = 40

class PSO(object):

    #data - paczka informacji wstepnych : N (rozmiar przestrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self):
        data=PARTICLES_COUNT,FUNCTION
        self.swarm= pso_swarm.Swarm(data)
        self.w=W

    # po to by sprawdzić jak zmniejszanie W wpływa na zbieganie do optimum globalnego (redukowanie eksploracji)
    def inertion_update_strategy(self):
        pass

    def run_iterations(self,verbose=True):
        for i in range(ITERATIONS_COUNT):
            self.swarm.pso_iteration_step(self.w,CP,CG)
            self.inertion_update_strategy()
            if(verbose):
                print('ITERATION '+str(i))
                print(self.swarm)

pso=PSO()
pso.run_iterations()
