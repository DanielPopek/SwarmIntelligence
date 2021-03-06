import copy

import pso_particle


class Swarm(object):

    # data - paczka informacji wstepnych : N (rozmiar przezstrzeni, minimum dziedziny benchmarku, maksiumum
    def __init__(self, data):
        # particles_count,N,benchmark_min,benchmark_max,cost_function=data
        particles_count, function = data
        N, benchmark_min, benchmark_max, cost_function = function.dim, function.minf, function.maxf, function.evaluate
        self.particles_count = particles_count
        self.cost_fuction = cost_function
        self.particles = self.initialize_particles(particles_count, N, benchmark_min, benchmark_max, cost_function)
        self.g = self.get_intitial_global_optimum()
        self.f = function
        self.best = self.g

    def initialize_particles(self, particles_count, N, benchmark_min, benchmark_max, cost_function):
        particles = []
        for i in range(particles_count):
            data = i, N, benchmark_min, benchmark_max, cost_function, self
            new_particle = pso_particle.Particle(data)
            particles.append(new_particle)
        return particles

    def get_intitial_global_optimum(self):
        g = self.particles[0].p[0]
        for i in range(self.particles_count):
            function_value = self.cost_fuction(self.particles[i].x[0])
            best_function_value = self.cost_fuction(g)
            if (function_value < best_function_value):
                g = self.particles[i].x[0]
        return g

    def update_global_optimum(self, particle):
        function_value = self.cost_fuction(particle.x[0])
        best_function_value = self.cost_fuction(self.g)
        if function_value < best_function_value:
            self.g = particle.x[0]

    def pso_iteration_step(self, w, cp, cg):
        for particle in self.particles:
            particle.update_velocity(w, cp, cg)
            particle.update_position()
            particle.update_local_optimum()
            self.update_global_optimum(particle)
        if self.cost_fuction(self.g) < self.cost_fuction(self.best):
            self.best = copy.deepcopy(self.g)

    def __str__(self):
        object = ''
        for i in range(self.particles_count):
            object += self.particles[i].__str__() + '\n'
        return object
