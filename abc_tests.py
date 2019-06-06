import statistics
import pandas as pd

from abc_main import *


fly_to_food_functions = [OnlookerBee.fly_to_food_simply, OnlookerBee.fly_to_food_uniformly_by_neighbour,
                         OnlookerBee.fly_to_food_choosing_random_dimensions,
                         OnlookerBee.fly_to_food_randomly_by_neighbour,
                         OnlookerBee.fly_to_food_uniformly_by_neighbourhood]
fly_to_food_fun = OnlookerBee.fly_to_food_choosing_random_dimensions

dimensions = [10]  # [2, 3, 5, 10, 25, 50]
benchmark_functions = [Ackley, Rastrigin, Schwefel]  # [Ackley, Rastrigin, Schwefel]
iterations = [200, 500, 1000]  # , 2000]  # , 1500, 2000]
bee_no = [50, 100, 500]
# limits = [10, 25, 50, 75, 100]
# neighbourhoods = [[0.1, 0.25, 0.5, 0.7], [0.25, 0.5, 1, 2], [10, 25, 50, 75, 100]]

n = 3

columns = ['i', 'f', 'dim', 'employed', 'onlookers', 'fly_to_food_fun', 'limit', 'neighbourhood', 'iter', 'best']

if __name__ == '__main__':
    for dim in dimensions:
        for f in benchmark_functions:
            f = f(dim)
            for i in iterations:
                file_name = f'{f.name}_{dim}D_{i}iters'
                df = pd.DataFrame(columns=columns)
                for empl_no in bee_no:
                    for onlook_no in bee_no:
                        # for fly_to_food_fun in fly_to_food_functions:
                        print(f'{f.name} {dim}D for {i} iters | {empl_no}/{onlook_no} bees')

                        # for l in limits:
                        #     # if fly_to_food_fun is OnlookerBee.fly_to_food_uniformly_by_neighbourhood:
                        #     #     if f.name == 'Schwefel':
                        #     #         neighbourhood = neighbourhoods[2]
                        #     #     else:
                        #     #         neighbourhood = neighbourhoods[1]
                        #     # else:
                        #     #     neighbourhood = neighbourhoods[0]
                        #     for neigh in neighbourhood:
                        limit = int(np.power(i, 2/3))
                        neigh = 0.2
                        for j in range(n):
                            print(f'    hive no {j+1}...')

                            hive = Hive(empl_no, onlook_no, f, fly_to_food_fun, limit, neigh)
                            best = run_abc(hive, i)[-1]

                            df = df.append({'i': j, 'f': f.name, 'dim': dim, 'employed': empl_no,
                                            'onlookers': onlook_no, 'fly_to_food_fun': fly_to_food_fun.__name__,
                                            'limit': limit, 'neighbourhood': neigh, 'iter': i, 'best': best},
                                           ignore_index=True)
                df.to_csv(file_name + '.csv')
