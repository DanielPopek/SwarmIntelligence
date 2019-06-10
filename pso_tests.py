import statistics
import pandas as pd
from benchmarks import *
from pso import *

W = 0.229 #0.729
CP = 1.49445
CG = 1.49445

FUNCTION = benchmarks.Rastrigin(2)
ITERATIONS_COUNT = 300
PARTICLES_COUNT = 50


# benchmark_functions = [Ackley(2), Rastrigin(2), Schwefel(2)]
# iterations = [200, 500, 1000]  # , 2000]  # , 1500, 2000]
benchmark_functions = [Rastrigin(2)]
iterations = [500, 1000]  # , 2000]  # , 1500, 2000]
particle_number = [50, 100, 500]
w_values=[0.1,0.3,0.5,0.7,1.0,1.5]
cp_values=[0.2,0.7,1.5,2.0,2.5,3.0]
cg_values=[0.2,0.7,1.5,2.0,2.5,3.0]


n = 3

columns = ['f','i', 'particles', 'w', 'cp', 'cg', 'limit', 'best']

if __name__ == '__main__':
    index=1;
    for function in benchmark_functions:
        for i in iterations:
            file_name = f'{function.name}_{i}iters'
            df = pd.DataFrame(columns=columns)
            for particle in particle_number:
                for w in w_values:
                    for cp in cp_values:
                        for cg in cg_values:
                            print(f'{index}:{function.name} for {i} iters | {particle} particles, w: {w}, cp: {cp}, cg: {cg}')
                            pso=PSO(particle,i,function,w,cp,cg)
                            best=pso.run_iterations(False)
                            df = df.append({'f': function.name, 'i': i, 'particles': particle,
                                            'w': w, 'cp': cp,
                                            'cg': cg, 'best': best},
                                           ignore_index=True)
                            index+=1
                df.to_csv(file_name + '.csv')