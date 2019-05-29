from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import scipy.optimize as so
import pickle

from benchmarks import *


def plot_rastrigin_3D(point=[0., 0.]):
    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (X ** 2 - 10 * np.cos(2 * np.pi * X)) + \
        (Y ** 2 - 10 * np.cos(2 * np.pi * Y)) + 20

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.nipy_spectral, linewidth=0.08, antialiased=True)

    x, y = [point[0]], [point[1]]
    z = 10 * len(x) + np.sum(np.power(x, 2) - 10 * np.cos(2 * np.pi * np.array(x)))
    ax.scatter(x, y, z, c='k')
    plt.savefig('rastrigin_function.png')
    plt.show()


def plot_rastrigin_2D3D():
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (X ** 2 - 10 * np.cos(2 * np.pi * X)) + \
        (Y ** 2 - 10 * np.cos(2 * np.pi * Y)) + 20

    surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, linewidth=0, cmap=cm.plasma)  # 3D

    ax = fig.add_subplot(1, 2, 2)
    c = plt.contourf(X, Y, Z, 10, cmap=cm.plasma)  # 2D

    circle_small = plt.Circle((0, 0), 0.05, color='k')  # center - optimum
    circle_big = plt.Circle((0, 0), 0.35, color='k', fill=False)
    ax.add_artist(circle_small)
    ax.add_artist(circle_big)

    # fig.colorbar(surf, aspect=18)
    plt.tight_layout()
    plt.show()


def animation_ackley_for_bees(file_name):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    X = np.arange(-20, 20, 0.25)
    Y = np.arange(-20, 20, 0.25)
    X, Y = np.meshgrid(X, Y)

    a = 20
    b = 0.2
    c = 2 * np.pi
    sum_sq_term = -a * np.exp(-b * np.sqrt(X*X + Y*Y) / 2)
    cos_term = -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
    Z = a + np.exp(1) + sum_sq_term + cos_term

    surf = ax.plot_surface(X, Y, Z, cmap=cm.summer, linewidth=0, antialiased=False)  # 3D

    ax = fig.add_subplot(1, 2, 2)
    c = plt.contourf(X, Y, Z, 25, cmap=cm.summer)  # 2D

    circle_small = plt.Circle((0, 0), 0.2, color='k')  # center - optimum
    circle_big = plt.Circle((0, 0), 1, color='k', fill=False)
    ax.add_artist(circle_small)
    ax.add_artist(circle_big)

    anim = animation_of_bees(fig, ax, file_name)

    plt.tight_layout()
    plt.show()


def animation_rastrigin_for_bees(file_name):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (X ** 2 - 10 * np.cos(2 * np.pi * X)) + \
        (Y ** 2 - 10 * np.cos(2 * np.pi * Y)) + 20

    surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, linewidth=0, cmap=cm.summer)  # 3D

    # ''' Animation 3D '''
    # line3D, = ax.plot([], [], [], 'ko')
    #
    # def init_3D():
    #     line3D.set_data([], [], [])
    #     return line3D,
    #
    # def animate_3D(i):
    #     line3D.set_data(res_x[i], res_y[i], res_z[i])
    #     return line3D,
    #
    # anim = animation.FuncAnimation(fig, animate_3D, init_func=init_3D, frames=len(res_x), interval=200, blit=True)
    # ''' End of 3D animation '''

    ax = fig.add_subplot(1, 2, 2)
    c = plt.contourf(X, Y, Z, 10, cmap=cm.summer)  # 2D

    circle_small = plt.Circle((0, 0), 0.05, color='k')  # center - optimum
    circle_big = plt.Circle((0, 0), 0.35, color='k', fill=False)
    ax.add_artist(circle_small)
    ax.add_artist(circle_big)

    anim = animation_of_bees(fig, ax, file_name)

    plt.tight_layout()
    plt.draw()
    plt.show()


def animation_schwefel_for_bees(file_name):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    X = np.linspace(-500, 500, 100)
    Y = np.linspace(-500, 500, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (-1 * X * np.sin(np.sqrt(abs(X)))) + (-1 * Y * np.sin(np.sqrt(abs(Y))));

    surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, linewidth=0, cmap=cm.summer)  # 3D

    # ''' Animation 3D '''
    # line3D, = ax.plot([], [], [], 'ko')
    #
    # def init_3D():
    #     line3D.set_data([], [], [])
    #     return line3D,
    #
    # def animate_3D(i):
    #     line3D.set_data(res_x[i], res_y[i], res_z[i])
    #     return line3D,
    #
    # anim = animation.FuncAnimation(fig, animate_3D, init_func=init_3D, frames=len(res_x), interval=200, blit=True)
    # ''' End of 3D animation '''

    ax = fig.add_subplot(1, 2, 2)
    c = plt.contourf(X, Y, Z, 15, cmap=cm.summer)  # 2D

    circle_small = plt.Circle((420.96, 420.96), 5, color='k')  # center - optimum
    circle_big = plt.Circle((420.96, 420.96), 20, color='k', fill=False)
    ax.add_artist(circle_small)
    ax.add_artist(circle_big)

    anim = animation_of_bees(fig, ax, file_name)

    plt.tight_layout()
    plt.draw()
    plt.show()


def animation_of_bees(fig, ax, file_name, save_gif=False):
    def load_bees_positions(file_name):
        with open("./tests/abc/" + file_name, "rb") as fp:
            x_best_bee, y_best_bee, x_empl, y_empl, x_onlook, y_onlook = pickle.load(fp)
        return x_best_bee, y_best_bee, x_empl, y_empl, x_onlook, y_onlook

    x_b, y_b, x_e, y_e, x_o, y_o = load_bees_positions(file_name)

    plot_colors, markers = ["orangered", "black", "#064413"], ["D", "X", "."]
    lines = []
    lines_data_x, lines_data_y = x_b + x_e + x_o, y_b + y_e + y_o

    line = ax.plot([], [], marker=markers[0], color=plot_colors[0])[0]  # for best bee
    lines.append(line)
    for bee in range(len(x_e)):
        line = ax.plot([], [], marker=markers[1], color=plot_colors[1])[0]  # for employed bees
        lines.append(line)
    for bee in range(len(x_o)):
        line = ax.plot([], [], marker=markers[2], color=plot_colors[2])[0]  # for onlooker bees
        lines.append(line)

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        for l, line in enumerate(lines):
            line.set_data(lines_data_x[l][i], lines_data_y[l][i])  # get bee, get current point
        return lines

    frames = len(lines_data_x[0])
    interval = int(8000/frames)
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=interval,
                                   blit=True, repeat=False)

    if save_gif:
        plt.tight_layout()
        anim.save('./tests/abc/' + file_name[:-4] + '.gif', writer='imagemagick', fps=60)

    return anim


if __name__ == '__main__':
    # file_name = 'Ackley_10-30_bees_in_100iterations_15limit_0.05neighbourhood.txt'
    # animation_ackley_for_bees(file_name)

    # file_name = 'Rastrigin_10-30_bees_in_100iterations_15limit_0.05neighbourhood.txt'
    # animation_rastrigin_for_bees(file_name)

    file_name = 'Schwefel_10-30_bees_in_100iterations_15limit_0.05neighbourhood.txt'
    animation_schwefel_for_bees(file_name)
