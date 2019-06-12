import statistics
import pandas as pd
from benchmarks import *
from cso import *


C= 3  #velocity update constant
MR=0.1 #percentage of cats in tracing mode
SMP=10 #observed points count
CDC=2 # changed dimentions count --contsant
SRD=0.3 #percentage of mutations
SPC=True # if self position considered

FUNCTION=benchmarks.Rastrigin(2)

ITERATIONS_COUNT = 100
CATS_COUNT = 40


benchmark_functions = [Rastrigin(2)]
iterations = [200]
cats_number = [50]
c_values=[0.5,1.0,1.5,2.0,3.0]
MR_values=[0.1,0.3,0.6,0.9]
SMP_values=[5,10,20,40]
SRD_values=[0.1,0.3,0.5,0.6]



n = 3

columns = ['f','i', 'cats', 'mr', 'c', 'smp', 'srd', 'best']

if __name__ == '__main__':
    index=1;
    for function in benchmark_functions:
        for i in iterations:
            file_name = f'CSO_{function.name}_{i}iters'
            df = pd.DataFrame(columns=columns)
            for cat in cats_number:
                for mr in MR_values:
                    for c in c_values:
                        for smp in SMP_values:
                            for srd in SRD_values:
                                print(f'{index}:{function.name} for {i} iters | {cat} cats, mr: {mr}, c: {c}, smp: {smp}, srd: {srd}')
                                cso=CSO(i,cat,function,mr,c,smp,2,srd,True)
                                best=cso.run_iterations(False)
                                df = df.append({'f': function.name, 'i': i, 'cats': cat,
                                                'mr': mr, 'c': c,
                                                'smp': smp,'srd':srd, 'best': best},
                                               ignore_index=True)
                                index+=1
                df.to_csv(file_name + '.csv')