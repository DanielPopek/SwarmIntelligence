from benchmarks import *
from abc_bees import *
import pickle


def update_bees_positions(x, y, bees, position=False):
    for i, bee in enumerate(bees):
        if position:
            x[i].append(bee[0])
            y[i].append(bee[1])
        else:
            x[i].append(bee.pos[0])
            y[i].append(bee.pos[1])
    return x, y


def save_bees_positions(x_best_bee, y_best_bee, x_empl, y_empl, x_onlook, y_onlook, hive, iterations):
    file_name = f"./tests/abc/{hive.f.name}_{hive.n_empl}-{hive.n_onlook}_bees_in_" \
        f"{iterations}iterations_{hive.LIMIT}limit_{hive.NEIGHBOURHOOD}neighbourhood.txt"
    with open(file_name, "wb") as fp:
        pickle.dump([x_best_bee, y_best_bee, x_empl, y_empl, x_onlook, y_onlook], fp)


if __name__ == '__main__':
    dimensions = 2
    benchmark_function = Schwefel(dimensions)
    employed_no, onlooker_no = 10, 30
    hive = Hive(employed_no, onlooker_no, benchmark_function)

    x_best_bee, y_best_bee = [[]], [[]]
    x_empl, y_empl = [[] for _ in range(employed_no)], [[] for _ in range(employed_no)]
    x_onlook, y_onlook = [[] for _ in range(onlooker_no)], [[] for _ in range(onlooker_no)]

    iterations = 100
    for i in range(iterations):
        print('Iteration', i)
        hive.roulette()  # get places to which onlookers should fly
        hive.update_onlookers_pos()
        hive.send_scouts_for_exploration_if_needed()

        if dimensions == 2:
            x_best_bee, y_best_bee = update_bees_positions(x_best_bee, y_best_bee, [hive.best_bee_pos], position=True)
            x_empl, y_empl = update_bees_positions(x_empl, y_empl, hive.bees_employed)
            x_onlook, y_onlook = update_bees_positions(x_onlook, y_onlook, hive.bees_onlookers)

    print('\nBest bee in the whole population:', hive.best_bee_pos)

    save_bees_positions(x_best_bee, y_best_bee, x_empl, y_empl, x_onlook, y_onlook, hive, iterations)
