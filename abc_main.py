from benchmarks import *
from abc_bees import *
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


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


def get_evaluation_values(hive):
    return [abs(hive.f.evaluate(bee.pos)) for bee in hive.bees_employed] + \
           [abs(hive.f.evaluate(bee.pos)) for bee in hive.bees_onlookers]


def best_and_avg_evaluation_plot(best_value, evaluation_values, iterations, f):
    best_bee = [min(values) for values in evaluation_values]
    avg_bee = [sum(values)/len(values) for values in evaluation_values]
    x = list(range(iterations))

    plt.plot(x, [0 for _ in x], color="grey", ls='--')
    plt.plot(x, best_bee, color='lightseagreen', label='best bee')
    plt.plot(x, best_value, color='forestgreen', label='best found')
    plt.plot(x, avg_bee, color='coral', label='average bee')
    plt.xlim(0, iterations-1)
    plt.legend()
    plt.ylabel('function value')
    plt.xlabel('iteration')

    best = best_value[-1]
    best_str = ('%0.8f' if best < 0.0001 else ('%0.5f' if best < 1 else ('%0.3f' if best < 10 else '%0.2f'))) % best
    plt.title(f'{f.name} function for ABC having {len(evaluation_values[0])} bees in {f.dim} dimensions\n'
              f'with final best value = {best_str}')

    plt.show()


if __name__ == '__main__':
    dimensions = 2
    benchmark_function = Schwefel(dimensions)
    employed_no, onlooker_no = 20, 50
    hive = Hive(employed_no, onlooker_no, benchmark_function)

    x_best_bee, y_best_bee = [[]], [[]]
    x_empl, y_empl = [[] for _ in range(employed_no)], [[] for _ in range(employed_no)]
    x_onlook, y_onlook = [[] for _ in range(onlooker_no)], [[] for _ in range(onlooker_no)]

    evaluation_values, best_value = [], []

    iterations = 200
    for i in range(iterations):
        if (i+1) % 25 == 0:
            print('Iteration', i+1)
        hive.roulette()  # get places to which onlookers should fly
        hive.update_onlookers_pos()
        hive.send_scouts_for_exploration_if_needed()

        evaluation_values.append(get_evaluation_values(hive))
        best_value.append(abs(benchmark_function.evaluate(hive.best_bee_pos)))

        if dimensions == 2:
            x_best_bee, y_best_bee = update_bees_positions(x_best_bee, y_best_bee, [hive.best_bee_pos], position=True)
            x_empl, y_empl = update_bees_positions(x_empl, y_empl, hive.bees_employed)
            x_onlook, y_onlook = update_bees_positions(x_onlook, y_onlook, hive.bees_onlookers)

    print('\nBest bee in the whole population:', hive.best_bee_pos)
    print('Evaluation:', abs(benchmark_function.evaluate(hive.best_bee_pos)))

    best_and_avg_evaluation_plot(best_value, evaluation_values, iterations, benchmark_function)

    if dimensions == 2:
        save_bees_positions(x_best_bee, y_best_bee, x_empl, y_empl, x_onlook, y_onlook, hive, iterations)
