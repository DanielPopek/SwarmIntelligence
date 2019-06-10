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


def plot_linear_by_iters_and_dim(algorithm, f, params={'employed': 100, 'onlookers': 100}):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4.5)
    colors = ['goldenrod', 'deeppink', 'deepskyblue', 'darkorchid', 'mediumseagreen', 'indianred', 'darkslategrey']

    dims = [2, 3, 5, 10, 50]
    file_names, iterations = [], []
    for dim in dims:
        file_name = [fn for fn in os.listdir(f'./tests/{algorithm}/csv/') if
                     fn.startswith(f'{f.name}_{dim}D_')]
        iteration = [int(f_name[(len(f.name) + len(str(f.dim)) + 3):-9]) for f_name in file_name]
        file_name = [x for _, x in sorted(zip(iteration, file_name))]
        iteration.sort()
        file_names.append(file_name)
        iterations.append(iteration)


    dfs = [[] for _ in len(dims)]
    for i, file_name in enumerate(file_names):
        for name in file_name:
            dfs[i].append(pd.read_csv(f'./tests/{algorithm}/csv/{name}', index_col=0))

    for d in len(dims):
        for i in range(len(dfs[d])):
            for key, value in params.items():
                dfs[d][i] = dfs[d][i].loc[dfs[d][i][key] == value]

    for i, d in enumerate(dims):
        y = [dfs[d][i]['best'].mean() for i in range(len(iterations[d]))]
        plt.plot(iterations[d], y, color=colors, marker='o')

    plt.legend()
    plt.show()


def plot_linear_by_params(algorithm, f, file_end, params={'neighbourhood': 0.1}, ylim=0):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4.5)
    colors = ['goldenrod', 'deeppink', 'deepskyblue', 'darkorchid', 'mediumseagreen', 'indianred']

    file_names = [filename for filename in os.listdir(f'./tests/{algorithm}/csv/')
                  if (filename.startswith(f'{f.name}_{f.dim}D_') and filename.endswith(file_end + '.csv'))]
    iterations = [int(f_name[(len(f.name) + len(str(f.dim)) + 3):(-9 - len(file_end) - 1)]) for f_name in file_names]
    file_names = [x for _, x in sorted(zip(iterations, file_names))]
    iterations.sort()

    dfs = []
    for name in file_names:
        dfs.append(pd.read_csv(f'./tests/{algorithm}/csv/{name}', index_col=0))

    all_params = ['neighbourhood', 'limit', 'fly_to_food_fun']
    for i in range(len(dfs)):
        for key, value in params.items():
            dfs[i] = dfs[i].loc[dfs[i][key] == value]
        if i == 0:
            all_params.remove(key)
    plot_by = all_params[0]

    y = np.array([dfs[i].groupby(plot_by)['best'].mean().values for i in range(len(iterations))])
    bees_values = dfs[0][plot_by].unique().tolist()
    np.set_printoptions(precision=20, suppress=True)
    for i, val in enumerate(bees_values):
        plt.plot(iterations, y[:, i], color=colors[i], label=str(val))
        print(f'{plot_by.upper()} = {val} --- {np.array(y[:, i])}')

    plt.title(f'{algorithm.upper()} for different {plot_by} values\n'
              f'{f.name} - {f.dim} dimensions')
    plt.xlabel('iterations')
    plt.xticks(iterations)
    plt.legend()
    if ylim > 0:
        plt.ylim(top=ylim, bottom=0 - ylim*0.01)
    plt.show()


if __name__ == '__main__':
    algorithm = 'abc'
    f = Ackley(10)

    # plot_linear_by_iters(algorithm, f, params={'employed': 100, 'onlookers': 100})
    plot_linear_by_params(algorithm, f, 'lim_neigh', params={'limit': 50}, ylim=0.001)

