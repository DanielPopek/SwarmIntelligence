import statistics
import pandas as pd
from benchmarks import *
from cso import *


benchmark_functions = [Ackley(2),Rastrigin(2)]
# iterations = [50,100,200,300,400,500,600,700,800,900,1000]
iterations = [10,20,30,40,50,60,70,80,90,100,120,130,140,150]
particles = [50,100,250,300,400,450]

def iteration_test():
    columns = ['f', 'i', 'best']
    for function in benchmark_functions:
        file_name = f'{function.name}_CSO_iterations_test'
        df = pd.DataFrame(columns=columns)
        for i in iterations:
            print(f'{function.name} for {i} iterations')
            cso = CSO(i, 50, function, 0.1, 0.5, 40, 2, 0.6, True)
            best = cso.run_iterations(False)
            df = df.append({'f': function.name, 'i': i,'best': best},ignore_index=True)
        df.to_csv(file_name + '.csv')

def particles_test():
    columns = ['f', 'p', 'best']
    for function in benchmark_functions:
        file_name = f'{function.name}_CSO_particles_test'
        df = pd.DataFrame(columns=columns)
        for p in particles:
            print(f'{function.name} for {p} particles')
            cso = CSO(200, p, function, 0.1, 0.5, 40, 2, 0.6, True)
            best = cso.run_iterations(False)
            df = df.append({'f': function.name, 'p': p,'best': best},ignore_index=True)
        df.to_csv(file_name + '.csv')

# iteration_test()
particles_test()
