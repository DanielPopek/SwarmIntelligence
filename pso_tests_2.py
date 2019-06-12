import statistics
import pandas as pd
from benchmarks import *
from pso import *


benchmark_functions = [Rastrigin(2)]
# iterations = [50,100,200,300,400,500,600,700,800,900,1000]
iterations = [10,20,30,40,50,60,70,80,90,100,120,130,140,150]
particles = [10,20,30,40,50,100,200,500]

def iteration_test():
    columns = ['f', 'i', 'best']
    for function in benchmark_functions:
        file_name = f'{function.name}_PSO_iterations_test'
        df = pd.DataFrame(columns=columns)
        for i in iterations:
            print(f'{function.name} for {i} iterations')
            pso=PSO(50,i,function,0.5,0.7,0.7)
            best=pso.run_iterations(False)
            df = df.append({'f': function.name, 'i': i,'best': best},ignore_index=True)
        df.to_csv(file_name + '.csv')

def particles_test():
    columns = ['f', 'p', 'best']
    for function in benchmark_functions:
        file_name = f'{function.name}_PSO_particles_test'
        df = pd.DataFrame(columns=columns)
        for p in particles:
            print(f'{function.name} for {p} particles')
            pso=PSO(p,100,function,0.5,0.7,0.7)
            best=pso.run_iterations(False)
            df = df.append({'f': function.name, 'p': p,'best': best},ignore_index=True)
        df.to_csv(file_name + '.csv')

# iteration_test()
particles_test()
