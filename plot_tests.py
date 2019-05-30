from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

from matplotlib import animation
from numpy import random
import scipy.optimize as so


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


def animation_rastrigin2():
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (X ** 2 - 10 * np.cos(2 * np.pi * X)) + \
        (Y ** 2 - 10 * np.cos(2 * np.pi * Y)) + 20

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

    # prepare data
    res_x = [4, 3.2, 3.1, 2.7, 2.6, 2.45, 2, 1.3, 1.1, 1.0, 0.3, 0.28, 0.24, 0.06, 0.05, 0]
    res_y = [4.2, 4.2, 4.1, 3.7, 3.3, 3.1, 2.5, 2.5, 2.1, 1.7, 1.4, 1.1, 0.9, 0.4, 0.2, 0]
    res_x2 = [4, 3.2, 3.1, 2.7, 2.6, 2.45, 2, 1.3, 1.1, 1.0, 0.3, 0.28, 0.24, 0.06, 0.05, 0]
    res_y2 = [-4.2, -4.2, -4.1, -3.7, -3.3, -3.1, -2.5, -2.5, -2.1, -1.7, -1.4, -1.1, -0.9, -0.4, -0.2, 0]

    plot_colors = ["black", "red"]
    lines = []
    lines_data = [[res_x, res_y], [res_x2, res_y2]]
    for index in range(len(plot_colors)):
        line = ax.plot([], [], marker='X', color=plot_colors[index])[0]
        lines.append(line)

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        for l, line in enumerate(lines):
            line.set_data(lines_data[l][0][i], lines_data[l][1][i])  # get data, get x/y, get current point
        return lines

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(res_x), interval=200, blit=True)

    # ''' Animation 2D no 2 '''
    # line2D2, = ax.plot([], [], 'ko')
    #
    # def init_2D2():
    #     line2D2.set_data([], [])
    #     return line2D2,
    #
    # def animate_2D2(i):
    #     line2D.set_data(res_x2[i], res_y2[i])
    #     return line2D2,
    #
    # anim = animation.FuncAnimation(fig, animate_2D2, init_func=init_2D2, frames=len(res_x2), interval=200, blit=True)

    plt.tight_layout()
    plt.show()


def test_animation_of_multiple_lines():
    fig = plt.figure()
    ax1 = plt.axes(xlim=(-108, -104), ylim=(31,34))

    # line, = ax1.plot([], [], lw=2)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plotlays, plotcols = [2], ["black", "red"]
    lines = []
    for index in range(2):
        lobj = ax1.plot([], [], lw=2, color=plotcols[index])[0]
        lines.append(lobj)

    def init():
        for line in lines:
            line.set_data([],[])
        return lines

    x1,y1 = [],[]
    x2,y2 = [],[]

    # fake data
    frame_num = 100
    gps_data = [-104 - (4 * random.rand(2, frame_num)), 31 + (3 * random.rand(2, frame_num))]


    def animate(i):
        x = gps_data[0][0, i]
        y = gps_data[1][0, i]
        x1.append(x)
        y1.append(y)

        x = gps_data[0][1, i]
        y = gps_data[1][1, i]
        x2.append(x)
        y2.append(y)

        xlist = [x1, x2]
        ylist = [y1, y2]

        #for index in range(0,1):
        for lnum,line in enumerate(lines):
            line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately.

        return lines

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=frame_num, interval=10, blit=False)


    plt.show()


if __name__ == '__main__':
    animation_rastrigin2()
