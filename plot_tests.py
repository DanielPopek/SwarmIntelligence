import pickle

from click._compat import raw_input
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

    file_names = [filename for filename in os.listdir(f'./tests/{algorithm}/csv/')
                  if (filename.startswith(f'{f.name}_{f.dim}D_') and filename.endswith('iters.csv'))]
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

    plt.title(f'{f.name} function {f.dim}D')
    plt.show()


def plot_linear_by_iters_and_bee(algorithm, f, plot_by='onlookers', other_bees=100, ylim=0):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4.5)
    colors = ['goldenrod', 'deeppink', 'deepskyblue', 'darkorchid', 'mediumseagreen', 'indianred', 'darkslategrey']

    file_names = [filename for filename in os.listdir(f'./tests/{algorithm}/csv/')
                  if (filename.startswith(f'{f.name}_{f.dim}D_') and filename.endswith('iters.csv'))]
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

    plt.title(f'{algorithm.upper()} for different {plot_by} number\n'
              f'{f.name} - {f.dim} dimensions')
    if ylim > 0:
        plt.ylim(top=ylim, bottom=0 - ylim*0.01)
    plt.legend(loc=1)
    plt.show()


def plot_linear_by_iters_and_dim(algorithm, f, params={'employed': 100, 'onlookers': 100}):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4.5)
    colors = ['goldenrod', 'deeppink', 'deepskyblue', 'darkorchid', 'mediumseagreen', 'indianred', 'darkslategrey']

    dims = [2, 3, 5, 10]
    file_names, iterations = [], []
    for dim in dims:
        file_name = [fn for fn in os.listdir(f'./tests/{algorithm}/csv/')
                     if (fn.startswith(f'{f.name}_{dim}D_') and fn.endswith('iters.csv'))]
        iteration = [int(f_name[(len(f.name) + len(str(dim)) + 3):-9]) for f_name in file_name]
        file_name = [x for _, x in sorted(zip(iteration, file_name))]
        iteration.sort()
        file_names.append(file_name)
        iterations.append(iteration)

    dfs = [[] for _ in range(len(dims))]
    for i, file_name in enumerate(file_names):
        for name in file_name:
            dfs[i].append(pd.read_csv(f'./tests/{algorithm}/csv/{name}', index_col=0))

    for d in range(len(dims)):
        for i in range(len(dfs[d])):
            for key, value in params.items():
                dfs[d][i] = dfs[d][i].loc[dfs[d][i][key] == value]

    for i, d in enumerate(dims):
        y = [dfs[i][j]['best'].mean() for j in range(len(iterations[i]))]
        plt.plot(iterations[i], y, color=colors[i], marker='o', label=str(d) + 'D')

    plt.title(f'{f.name} function for different dimensions')
    plt.legend()
    plt.show()


def plot_linear_by_params(algorithm, f, file_end, params={'neighbourhood': 0.1}, ylim=0, leg=True):
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

    all_params = ['neighbourhood', 'limit'] if file_end == 'lim_neigh' else ['fly_to_food_fun']
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
        if file_end == 'fun':
            val = val[12:]
        plt.plot(iterations, y[:, i], color=colors[i], label=str(val))
        print(f'{plot_by.upper()} = {val} --- {np.array(y[:, i])}')

    plt.title(f'{algorithm.upper()} for different {plot_by} values\n'
              f'{f.name} - {f.dim} dimensions')
    plt.xlabel('iterations')
    plt.xticks(iterations)
    if leg:
        plt.legend()
    if ylim > 0:
        plt.ylim(top=ylim, bottom=0 - ylim*0.01)
    plt.show()


def plot_iters_test(algorithm, f, params={'employed': 100, 'onlookers': 100}):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 4.5)
    colors = ['goldenrod', 'deeppink', 'deepskyblue', 'darkorchid', 'mediumseagreen', 'indianred']

    file_names = [filename for filename in os.listdir(f'./tests/{algorithm}/csv/')
                  if (filename.startswith(f'{f.name}_{f.dim}D_') and filename.endswith('iters.csv'))]
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

    plt.title(f'{f.name} function {f.dim}D')
    plt.show()

def plot_iters_impact(file_name,fun,alg):
    data = pd.read_csv(file_name).iloc[:, 1:]
    fig, ax = plt.subplots()
    iters=data['i']
    best=data['best']
    plt.plot(iters, best, label="iterations", marker='o')
    plt.legend()
    plt.title(f'{alg}, {fun} function, iterations test ')
    plt.show()
    fig.savefig(file_name[:-4] + '_PLOT.png', dpi=150)

def plot_particles_impact(file_name,fun,alg):
    data = pd.read_csv(file_name).iloc[:, 1:]
    fig, ax = plt.subplots()
    particles=data['p']
    best=data['best']
    plt.plot(particles, best, label="cats count", marker='o')
    plt.legend()
    plt.title(f'{alg}, {fun} function, particles test ')
    plt.show()
    fig.savefig(file_name[:-4] + '_PLOT.png', dpi=150)


# def plot_heat_map(filepath):
#     df= pd.read_csv(filepath ,index_col=0)
#     df=df.drop(['f', 'i','cats'], axis=1)
#     print(df)
#     plt.imshow(df,cmap='hot',interpolation='nearest')
#     plt.show()


if __name__ == '__main__':
    plot_particles_impact('Rastrigin_CSO_particles_test.csv','Rastrigin','CSO')
    # plot_heat_map('./tests/cso/csv/CSO_Ackley_200iters.csv')
    # f = Rastrigin(2)
    #
    # ''' PSO '''
    # algorithm = 'pso'
    # plot_linear_by_iters(algorithm, f, params={'w': 0.5, 'cp': 0.2, 'cg': 0.2})
    #
    # ''' ABC '''
    # algorithm = 'abc'
    # plot_linear_by_iters_and_dim(algorithm, f)
    # plot_linear_by_iters(algorithm, f, params={'employed': 50, 'onlookers': 200})
    # plot_linear_by_iters_and_bee(algorithm, f, plot_by='employed', other_bees=10, ylim=0)
    # plot_linear_by_params(algorithm, f, 'lim_neigh', params={'neighbourhood': 0.1}, ylim=0)
    # plot_linear_by_params(algorithm, f, 'fun', params={}, ylim=0, leg=True)

    # import pylab
    # import time
    # import random
    # import matplotlib.pyplot as plt
    #
    # dat = [0, 1]
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # Ln, = ax.plot(dat)
    # ax.set_xlim([0, 20])
    # plt.ion()
    # plt.show()
    # for i in range(18):
    #     dat.append(random.uniform(0, 1))
    #     Ln.set_ydata(dat)
    #     Ln.set_xdata(range(len(dat)))
    #     plt.pause(1)
    #
    #     print('done with loop')

# fly_to_fun_simply
# 100 / 50 limit
# 0.5 neighbourhood
