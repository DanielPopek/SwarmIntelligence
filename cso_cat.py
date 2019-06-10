import numpy as np


class Cat(object):

    # data - paczka informacji wstepnych : N (rozmiar przezstrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self, data):
        index, N, benchmark_min, benchmark_max, cost_function, swarm, tracing, c, smp, cdc, srd, spc = data
        self.swarm = swarm
        self.index = index
        self.cost_fuction = cost_function
        self.x, self.v = self.initialize_positions_and_velocity(N, benchmark_min, benchmark_max)
        self.SPC = spc
        self.SMP = smp
        self.SRD = srd
        self.CDC = cdc
        self.c=c
        self.tracing = tracing
        self.N = N
        self.benchmark_min=benchmark_min
        self.benchmark_max=benchmark_max

    def initialize_positions_and_velocity(self, N, benchmark_min, benchmark_max):
        position = np.zeros(shape=(1, N))
        velocity = np.zeros(shape=(1, N))
        for i in range(N):
            position[0, i] = np.random.uniform(benchmark_min, benchmark_max, 1)[0]
            velocity[0, i] = np.random.uniform(-(benchmark_max - benchmark_min), benchmark_max - benchmark_min, 1)[0]
        return position, velocity

    def update_position_seeking_mode(self):
        candidates_count = self.SMP
        if (self.SPC):
            candidates_count -= 1
        candidates = np.repeat(self.x, candidates_count, axis=0)
        # print(candidates)
        for i in range(candidates_count):
            for j in range(self.CDC):
                old_val = candidates[i, j]
                new_val=np.random.uniform(old_val-abs(self.SRD * old_val), old_val+abs(self.SRD * old_val), 1)[0]
                candidates[i, j] = new_val
        candidates=np.reshape(candidates, newshape=(candidates_count,self.N))
        if (self.SPC):
            candidates = np.append(candidates, self.x)
            candidates = np.reshape(candidates, newshape=(candidates_count+1, self.N))
        fitess_values = [self.cost_fuction(np.reshape(candidates[i],newshape=(1,self.N))) for i in range(candidates_count)]
        f_max = max(fitess_values)
        f_min = min(fitess_values)
        probs = [0 for i in range(candidates_count)]
        if (f_min != f_max):
            probs = [abs(fitess_values[i] - f_max) / (f_max - f_min) for i in range(candidates_count)]
        probs_sum=np.sum(probs)
        normalized_probs=probs/probs_sum
        new_position = np.random.choice([i for i in range(candidates_count)], p=normalized_probs)
        self.x = np.reshape(candidates[new_position],newshape=(1,self.N))
        return self.x

    def update_position_tracing_mode(self):
        self.update_velocity()
        self.update_position_velocity()

    def update_position(self):
        if (self.tracing):
            self.update_position_tracing_mode()
        else:
            self.update_position_seeking_mode()

    def update_velocity(self):
        r = np.random.uniform(0, 1, 1)[0]
        v_new = self.v + self.c * r * (self.swarm.g - self.x)
        self.v = v_new

    def update_position_velocity(self):
        self.x += self.v
        for i in range(self.N):
            if self.x[0, i]>self.benchmark_max :
                self.x[0,i]=self.benchmark_max
            if self.x[0, i]<self.benchmark_min:
                self.x[0, i] = self.benchmark_min

    def __str__(self):
        return 'cat: {0}, position: {1}, tracing: {2} '.format(self.index, self.x,self.tracing)