import pickle

from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

from matplotlib import animation
from numpy import random
import scipy.optimize as so
import os
import pandas as pd
import seaborn as sns
sns.set()

from benchmarks import *


def plot_linear_by_iters(algorithm, f, params={'employed': 100, 'onlookers': 100}):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4.5)
    colors = ['goldenrod', 'deeppink', 'deepskyblue', 'darkorchid', 'mediumseagreen', 'indianred']

    file_names = [filename for filename in os.listdir(f'./tests/{algorithm}/csv/') if filename.startswith(f'{f.name}_{f.dim}D_')]
    iterations = [int(f_name[(len(f.name) + len(str(f.dim)) + 3):-9]) for f_name in file_names]
    file_names = [x for _, x in sorted(zip(iterations, file_names))]
    iterations.sort()

    dfs = []
    for name in file_names:
        dfs.append(pd.read_csv(f'./tests/{algorithm}/csv/{name}', index_col=0))

    for i in range(len(dfs)):
        for key, value in params.items():
            dfs[i] = dfs[i].loc[dfs[i][key] == value]

    y = [dfs[i]['best'].mean() for i in range(len(iterations))]
    plt.plot(iterations, y, color='deeppink', marker='o')

    plt.show()


def plot_linear_by_iters_and_bee(algorithm, f, plot_by='onlookers', other_bees=100):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4.5)
    colors = ['goldenrod', 'deeppink', 'deepskyblue', 'darkorchid', 'mediumseagreen', 'indianred', 'darkslategrey']

    file_names = [filename for filename in os.listdir(f'./tests/{algorithm}/csv/') if
                  filename.startswith(f'{f.name}_{f.dim}D_')]
    iterations = [int(f_name[(len(f.name) + len(str(f.dim)) + 3):-9]) for f_name in file_names]
    file_names = [x for _, x in sorted(zip(iterations, file_names))]
    iterations.sort()

    dfs = []
    for name in file_names:
        dfs.append(pd.read_csv(f'./tests/{algorithm}/csv/{name}', index_col=0))

    params = ['employed', 'onlookers']
    params.remove(plot_by)
    for i in range(len(dfs)):
        for bee in params:
            dfs[i] = dfs[i].loc[dfs[i][bee] == other_bees]

    y = np.array([dfs[i].groupby(plot_by)['best'].mean().values for i in range(len(iterations))])
    bees_values = dfs[0][plot_by].unique().tolist()
    for i, val in enumerate(bees_values):
        plt.plot(iterations, y[:, i], color=colors[i], label=str(val))

    plt.legend()
    plt.show()


if __name__ == '__main__':
    algorithm = 'abc'
    f = Ackley(2)

    # plot_linear_by_iters(algorithm, f, params={'employed': 100, 'onlookers': 100})
    plot_linear_by_iters_and_bee(algorithm, f)

