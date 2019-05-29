import numpy as np

from scipy import optimize
from deap.benchmarks import schwefel

from abc import ABCMeta
from abc import abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class ObjectiveFunction(object):

    def __init__(self, name, dim, minf, maxf):
        self.name = name
        self.dim = dim
        self.minf = minf
        self.maxf = maxf

    def sample(self):
        return np.random.uniform(low=self.minf, high=self.maxf, size=self.dim)

    def custom_sample(self):
        return np.repeat(self.minf, repeats=self.dim) \
               + np.random.uniform(low=0, high=1, size=self.dim) *\
               np.repeat(self.maxf - self.minf, repeats=self.dim)

    @abstractmethod
    def evaluate(self, x):
        pass


class Rastrigin(ObjectiveFunction):

    def __init__(self, dim):
        super(Rastrigin, self).__init__('Rastrigin', dim, -5.12, 5.12)

    def evaluate(self, x):
        return 10 * len(x)\
               + np.sum(np.power(x, 2) - 10 * np.cos(2 * np.pi * np.array(x)))


class Schwefel(ObjectiveFunction):

    def __init__(self, dim):
        super(Schwefel, self).__init__('Schwefel', dim, -500.0, 500.0)

    def evaluate(self, x):
        return schwefel(x)[0]


class Ackley(ObjectiveFunction):

    def __init__(self, dim):
        super(Ackley, self).__init__('Ackley', dim, -25.0, 25.0)

    def evaluate(self, x):
        first_sum = 0.0
        second_sum = 0.0
        for c in x:
            first_sum += c ** 2.0
            second_sum += np.math.cos(2.0 * np.math.pi * c)
        n = float(len(x))
        return -20.0 * np.math.exp(-0.2 * np.math.sqrt(first_sum / n)) - np.math.exp(second_sum / n) + 20 + np.math.e
