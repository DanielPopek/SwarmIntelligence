from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import scipy.optimize as so


def plot_rastrigin_3D():
    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (X ** 2 - 10 * np.cos(2 * np.pi * X)) + \
        (Y ** 2 - 10 * np.cos(2 * np.pi * Y)) + 20

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.nipy_spectral, linewidth=0.08, antialiased=True)

    x, y = [1.98377393], [-0.02871249]
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


def animation_test():

    def Gen_RandLine(length, dims=2):
        """
        Create a line using a random walk algorithm

        length is the number of points for the line.
        dims is the number of dimensions the line has.
        """
        lineData = np.empty((dims, length))
        lineData[:, 0] = np.random.rand(dims)
        for index in range(1, length):
            # scaling the random numbers by 0.1 so
            # movement is small compared to position.
            # subtraction by 0.5 is to change the range to [-0.5, 0.5]
            # to allow a line to move backwards.
            step = ((np.random.rand(dims) - 0.5) * 0.1)
            lineData[:, index] = lineData[:, index - 1] + step

        return lineData

    def update_lines(num, dataLines, lines):
        for line, data in zip(lines, dataLines):
            # NOTE: there is no .set_data() for 3 dim data...
            line.set_data(data[0:2, :num])
            line.set_3d_properties(data[2, :num])
        return lines

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # Fifty lines of random 3-D lines
    data = [Gen_RandLine(40, 3) for index in range(5)]

    # Creating fifty line objects.
    # NOTE: Can't pass empty arrays into 3d version of plot()
    lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
                                       interval=50, blit=False)

    plt.show()


def animation_2_test():
    fig = plt.figure()
    ax = plt.axes(xlim=(-0.5, 3.5), ylim=(-10, 100))
    line, = ax.plot([], [], 'o')

    def F(x):
        return (x ** 3 - x ** 2 - 9.) ** 2

    # get the optimize progress
    res_x = []
    so.fmin(F, -9, callback=res_x.append)
    res_x = np.array(res_x).ravel()
    res_y = F(res_x)

    def init():
        line.set_data([], [])
        return line,

    # animation function - this is called sequentially
    def animate(i):
        line.set_data(res_x[i], res_y[i])
        return line,

    ax.plot(np.linspace(0, 10, 100), F(np.linspace(0, 10, 100)), 'g')
    # frames is the length of res_x
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(res_x), interval=200, blit=True)
    plt.show()


def animation_rastrigin():
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (X ** 2 - 10 * np.cos(2 * np.pi * X)) + \
        (Y ** 2 - 10 * np.cos(2 * np.pi * Y)) + 20

    # get the optimize progress
    res_x = [4, 3.2, 3.1, 2.7, 2.6, 2.45, 2, 1.3, 1.1, 1.0, 0.3, 0.28, 0.24, 0.06, 0.05, 0]
    res_y = [4.2, 4.2, 4.1, 3.7, 3.3, 3.1, 2.5, 2.5, 2.1, 1.7, 1.4, 1.1, 0.9, 0.4, 0.2, 0]
    res_z = [70, 53, 43, 40, 39, 37, 34, 30, 30, 23, 22, 21, 18, 15, 10, 8, 1]

    surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, linewidth=0, cmap=cm.plasma)  # 3D

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
    c = plt.contourf(X, Y, Z, 10, cmap=cm.plasma)  # 2D

    circle_small = plt.Circle((0, 0), 0.05, color='k')  # center - optimum
    circle_big = plt.Circle((0, 0), 0.35, color='k', fill=False)
    ax.add_artist(circle_small)
    ax.add_artist(circle_big)

    ''' Animation 2D '''
    line2D, = ax.plot([], [], 'kx')

    def init_2D():
        line2D.set_data([], [])
        return line2D,

    def animate_2D(i):
        line2D.set_data(res_x[i], res_y[i])
        return line2D,

    anim = animation.FuncAnimation(fig, animate_2D, init_func=init_2D, frames=len(res_x), interval=200, blit=True)

    plt.tight_layout()
    plt.show()


def animation_3_test():
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 4)

    t = np.linspace(0, 80, 300)
    x = np.cos(2 * np.pi * t / 10.)
    y = np.sin(2 * np.pi * t / 10.)
    z = 10 * t

    lines = []
    for i in range(len(t)):
        head = i - 1
        head_slice = (t > t[i] - 1.0) & (t < t[i])
        # print(x[head],y[head],z[head])
        line1, = ax1.plot(x[:i], y[:i], z[:i],
                          color='black')
        line1a, = ax1.plot(x[head_slice], y[head_slice], z[head_slice],
                           color='red', linewidth=2)
        line1e, = ax1.plot([x[head]], [y[head]], [z[head]],
                           color='red', marker='o', markeredgecolor='r')
        line2, = ax2.plot(y[:i], z[:i],
                          color='black')
        line2a, = ax2.plot(y[head_slice], z[head_slice],
                           color='red', linewidth=2)
        line2e, = ax2.plot(y[head], z[head],
                           color='red', marker='o', markeredgecolor='r')
        line3, = ax3.plot(x[:i], z[:i],
                          color='black')
        line3a, = ax3.plot(x[head_slice], z[head_slice],
                           color='red', linewidth=2)
        line3e, = ax3.plot(x[head], z[head],
                           color='red', marker='o', markeredgecolor='r')
        lines.append([line1, line1a, line1e, line2, line2a, line2e, line3, line3a, line3e])

    plt.tight_layout()
    ani = animation.ArtistAnimation(fig, lines, interval=50, blit=True)
    plt.show()


if __name__ == '__main__':
    plot_rastrigin_3D()
    # animation_rastrigin()

    # [0.21215191 -0.89698555  1.73341022]
