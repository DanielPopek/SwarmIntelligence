from benchmarks import *
from abc_bees import *


if __name__ == '__main__':
    benchmark_function = Ackley(5)  # 2 dimensions for tests

    no_of_bees = 50
    hive = Hive(no_of_bees, benchmark_function)

    iterations = 200
    for i in range(iterations):
        print('\nITERATION', i)
        hive.roulette()  # get places to which onlookers should fly
        hive.update_onlookers_pos()
        hive.send_scouts_for_exploration_if_needed()

    print('\nBest bee in whole population:', hive.best_bee_pos)
