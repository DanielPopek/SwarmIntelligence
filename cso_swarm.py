import cso_cat
import numpy as np
import random
import  copy

class CatSwarm(object):

    #data - paczka informacji wstepnych : N (rozmiar przezstrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self,data):
        cats_count, function, MR, c, smp, cdc, srd, spc = data
        self.mr,self.c,self.smp,self.cdc,self.srd,self.spc=MR, c, smp, cdc, srd, spc
        N, benchmark_min, benchmark_max,cost_function=function.dim,function.minf,function.maxf,function.evaluate
        self.N=N
        self.cats_count=cats_count
        self.cost_fuction = cost_function
        self.cats=self.initialize_cats(cats_count,N,benchmark_min,benchmark_max,cost_function,c, smp, cdc, srd, spc)
        self.g=self.get_intitial_global_optimum()
        self.best=copy.deepcopy(self.g)


    def initialize_cats(self,cats_count,N,benchmark_min,benchmark_max,cost_function, c, smp, cdc, srd, spc):
        cats=[]
        tracing_count=int(self.mr*self.cats_count)
        for i in range(tracing_count):
            data=i,N,benchmark_min,benchmark_max,cost_function,self,True,c, smp, cdc, srd, spc
            new_cat= cso_cat.Cat(data)
            cats.append(new_cat)
        for i in range(tracing_count,self.cats_count):
            data = i, N, benchmark_min, benchmark_max, cost_function, self, False, c, smp, cdc, srd, spc
            new_cat = cso_cat.Cat(data)
            cats.append(new_cat)
        return cats

    def get_intitial_global_optimum(self):
        g=self.cats[0].x
        for i in range(self.cats_count):
            function_value=self.cost_fuction(self.cats[i].x)
            best_function_value = self.cost_fuction(g)
            if(function_value<best_function_value):
                g=self.cats[i].x
        return g

    def update_global_optimum(self):
        g=self.cats[0].x
        for i in range(self.cats_count):
            function_value=self.cost_fuction(np.reshape(self.cats[i].x,newshape=(1,self.N)))
            best_function_value = self.cost_fuction(g)
            if(function_value<best_function_value):
                g = self.cats[i].x
        self.g=g

    def change_cats_modes(self):
        tracing_count=int(self.mr*self.cats_count)
        for i in range(self.cats_count) :
            self.cats[i].tracing=False
        chosen_indexes=np.random.choice(self.cats_count, tracing_count)
        for i in chosen_indexes:
            self.cats[i].tracing=True

    def cso_iteration_step(self):
        for cat in self.cats:
            cat.update_position()
            self.update_global_optimum()
        self.change_cats_modes()
        if self.cost_fuction(self.g) < self.cost_fuction(self.best):
            self.best = copy.deepcopy(self.g)

    def __str__(self):
        object=''
        for i in range(self.cats_count):
            object+=self.cats[i].__str__()+'\n'
        object+=str(self.best)
        return object