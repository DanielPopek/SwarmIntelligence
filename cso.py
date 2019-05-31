import cso_swarm
import benchmarks

C= 1.5
MR=0.1
SMP=10
CDC=2
SRD=0.3
SPC=True

FUNCTION=benchmarks.SampleFunction(2)

ITERATIONS_COUNT = 100
CATS_COUNT = 40

class CSO(object):

    #data - paczka informacji wstepnych : N (rozmiar przestrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self):
        data=CATS_COUNT,FUNCTION,MR, C, SMP, CDC, SRD, SPC
        self.swarm= cso_swarm.CatSwarm(data)

    def run_iterations(self,verbose=True):
        for i in range(ITERATIONS_COUNT):
            self.swarm.cso_iteration_step()
            if(verbose):
                print('ITERATION '+str(i))
                print(self.swarm)
                print(self.swarm.g)

cso=CSO()
cso.run_iterations()

