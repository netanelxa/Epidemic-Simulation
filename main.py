import time
from tkinter import messagebox

import CreatureMatrix
import matplotlib
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cycler, gridspec
import matplotlib.animation as animation

import MainWindow

try:
    mpl.use('Qt5Agg')
    mpl.rcParams['toolbar'] = 'None'
except ValueError as e:
    print('Error: matplotlib backend\n', e)
    print('Trying:', mpl.get_backend())
    mpl.use(matplotlib.get_backend())

repeats = 10


class Grid:
    def __init__(self, grid, creature_number, probToInfect, k, newK, AfterMoves):

        self.creatures = {}
        global repeats
        if k == -1:

            repeats = 8
            for i in range(repeats):
                self.creatures[i] = {}

                self.creatures[i]["obj"] = CreatureMatrix.matrixHandler(grid, creature_number - 1, 1, probToInfect,
                                                                        i,
                                                                        newK,
                                                                        AfterMoves)
                self.creatures[i]["mats"] = list()
                self.creatures[i]["lines"] = []
                self.creatures[i]["growth"] = []
                self.creatures[i]["difference"] = []
                self.creatures[i]["average"] = 0
                self.creatures[i]["healthy"] = []
                self.creatures[i]["infected"] = []
        else:

            for i in range(repeats):
                self.creatures[i] = {}
                self.creatures[i]["obj"] = CreatureMatrix.matrixHandler(grid, creature_number - 1, 1, probToInfect, k,
                                                                        newK,
                                                                        AfterMoves)
                self.creatures[i]["mats"] = list()
                self.creatures[i]["lines"] = []
                self.creatures[i]["growth"] = []
                self.creatures[i]["average"] = 0
                self.creatures[i]["healthy"] = []
                self.creatures[i]["infected"] = []

        self.dim = grid
        self.creature_size = creature_number

    def init_grid(self):

        average = 0
        for i in self.creatures:
            mat = self.creatures[i]["obj"]
            percent = mat.getNumOfInfected() / (mat.getNumOfInfected() + mat.getNumOfHealthy())
            percent_of_infected = 0
            start = time.time()
            while percent != 1:
                healthy, infected = mat.moveAllOneStep()
                self.creatures[i]["healthy"].append(healthy)
                self.creatures[i]["infected"].append(infected)
                self.creatures[i]["lines"].append(mat.getNumOfInfected())
                percent = mat.getNumOfInfected() / (mat.getNumOfInfected() + mat.getNumOfHealthy())

                if percent_of_infected != int(percent * 100):
                    percent_of_infected = int(percent * 100)
                    # sliders[i].set_val(percent_of_infected)
                    print(str(percent_of_infected) + "% " + str(i))
            end = time.time()
            total_time = end - start
            print(str(i) + " finished within " + str(round(total_time, 2)))
            average += total_time / repeats

        max_frames = max([len(self.creatures[m]["lines"]) for m in self.creatures])
        self.frames = max_frames
        for i in self.creatures:
            for n in range(max_frames - len(self.creatures[i]["lines"])):
                healthy, infected = self.creatures[i]["obj"].moveAllOneStep()
                self.creatures[i]["healthy"].append(healthy)
                self.creatures[i]["infected"].append(infected)
                self.creatures[i]["lines"].append(self.creatures[i]["obj"].getNumOfInfected())
            tframe = len(self.creatures[i]["mats"])
        # print("Average time: " + str(round(average, 2)))


def main():
    # Matrix Animation
    global repeats
    interval = 50
    experimentSets = [[200, 80, 0], [500, 80, 0], [1000, 80, 0], [500, 35, 0], [500, 70, 0], [500, 95, 0], [200, 35, 0],
                      [1000, 99, 0], [500, 80, 2], [500, 80, 5], [500, 80, 7]]
    UserChoose = MainWindow.MainWindow(experimentSets)
    ## Matrix Animation ##
    grid = 200
    newK = 0
    AfterMoves = -1
    if len(UserChoose.paramters) == 3:
        creatures = int(UserChoose.paramters[0])
        infection_chance = int(UserChoose.paramters[1])
        k = int(UserChoose.paramters[2])
    else:
        newK = int(UserChoose.paramters[0])
        AfterMoves = int(UserChoose.paramters[1])
        creatures = int(UserChoose.paramters[2])
        infection_chance = int(UserChoose.paramters[3])
        k = int(UserChoose.paramters[4])

    G = Grid(grid, creatures, infection_chance, k, newK, AfterMoves)
    G.init_grid()

    mpl.rcParams['savefig.pad_inches'] = 0
    plt.rcParams['toolbar'] = 'None'

    fig = plt.figure("PLOT_CLUSTER_A")
    fig.set_size_inches(12, 7.5, True)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)

    gs0 = gridspec.GridSpec(1, 8, figure=fig, wspace=4)

    gs00 = gridspec.GridSpecFromSubplotSpec(5, 5, subplot_spec=gs0[0:5])
    gs01 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs0[5:8], hspace=0.4)

    axes = []
    parts = []

    little_matrix_grid = [gs00[0:4, 0:4], gs00[0, 4], gs00[1, 4], gs00[2, 4], gs00[3, 4], gs00[4, 4], gs00[4, 3],
                          gs00[4, 2], gs00[4, 1], gs00[4, 0]]
    for i in range(repeats):
        ax1 = fig.add_subplot(little_matrix_grid[i], xlim=(0, G.dim), ylim=(0, G.dim), autoscale_on=False)
        ax1.axis('off')
        axes.append(ax1)

        particles, = axes[i].plot([], [], 'bo', ms=6, marker='o', c="green", mec="black", animated=True)
        particles2, = axes[i].plot([], [], 'bo', ms=6, marker='o', c="red", mec="black", animated=True)

        parts.extend([particles, particles2])

        ## LINE PLOT ##

    cmap = plt.cm.Paired
    matplotlib.rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, repeats)))

    ax_linear = fig.add_subplot(gs01[0])
    ax_growth = fig.add_subplot(gs01[2])
    ax_exponential = fig.add_subplot(gs01[1])

    for i in range(repeats):
        linear_line, = (ax_linear.plot(np.arange(G.frames), G.creatures[i]["lines"], linewidth=1, linestyle='solid',
                                       solid_capstyle='round', label=str(i)))
        parts.append(linear_line)

    ax_linear.set_title('Cumulative Graph of Infected Creatures', fontsize=8)
    ax_linear.set_xlabel('Generation', fontsize=8)
    ax_linear.set_ylabel('Total Number of Infected Creatures', fontsize=8)
    ax_linear.grid(True)
    ax_linear.legend(fontsize='x-small', ncol=2, loc='lower right')
    ax_linear.tick_params(axis='both', which='major', labelsize=8)

    # Growth
    span = 40
    max_height = 0
    for i in range(repeats):
        f = np.concatenate(([0], G.creatures[i]["lines"]))
        f = np.diff(f)
        for j in range(len(f)):
            if j - span < 0:
                G.creatures[i]["growth"].append(np.sum(np.concatenate(((span - j) * [0], f[:j + span]))))
            elif len(f) <= j + span:
                G.creatures[i]["growth"].append(np.sum(f[j - span:]))
            else:
                G.creatures[i]["growth"].append(np.sum(f[j - span:j + span]))

        max_height = max(max_height, max(G.creatures[i]["growth"]))

        growth_line, = (
            ax_growth.plot(np.arange(G.frames), G.creatures[i]["growth"], linewidth=1, linestyle='solid',
                           solid_capstyle='round', label=str(i)))
        parts.append(growth_line)

    ax_growth.set_title('Growth Rate of Infected Creatures', fontsize=8)
    ax_growth.set_xlabel('Generation', fontsize=8)
    ax_growth.set_ylabel('Current Number of Infected Creatures', fontsize=8)
    ax_growth.set_yscale("log", basey=2)
    ax_growth.grid(True)
    ax_growth.legend(fontsize='x-small', ncol=2)
    ax_growth.tick_params(axis='both', which='major', labelsize=8)

    for i in range(repeats):
        g = np.concatenate(([0], G.creatures[i]["growth"]))
        g = np.diff(g)


    for i in range(repeats):
        exponential_line, = (
            ax_exponential.plot(np.arange(G.frames), G.creatures[i]["lines"], linewidth=1, linestyle='solid',
                                solid_capstyle='round', label=str(i)))
        parts.append(exponential_line)

    ax_exponential.set_title('Y Scaled Logarithmic Graphs', fontsize=8)
    ax_exponential.set_xlabel('Generation', fontsize=8)
    ax_exponential.set_ylabel('Number of infected creatures', fontsize=8)
    ax_exponential.set_yscale("log", basey=2)
    ax_exponential.grid(True)
    ax_exponential.legend(fontsize='x-small', ncol=2)
    ax_exponential.tick_params(axis='both', which='major', labelsize=8)

    def init():
        for i in range(repeats * 5):
            parts[i].set_data([], [])

        return parts

    def animate(frame):
        if frame % G.mod == 0:
            intervalCounter = int(frame / 10) + 1
            for index in range(repeats):
                numOfInfected = G.creatures[index]["lines"][frame]
                numofHealthy = G.creature_size - numOfInfected
                if (index not in G.flag):
                    print("Interval Number " + str(intervalCounter) + " Matrix Number " + str(
                        index + 1) + " Num of infected - " + str(numOfInfected) + " Num of healthy - " + str(
                        numofHealthy) + " percent of infected " + str(int((numOfInfected / G.creature_size * 100))))
                if numofHealthy == 0 and (index not in G.flag):
                    G.flag.append(index)
                    timeElapsed = float("{:.3f}".format(time.time() - G.starttime))
                    print("All have been infected in matrix " + str(index + 1) + " in " + str(timeElapsed) + (" sec"))
                    G.timeList.append(timeElapsed)
                    if len(G.flag) == 8:
                        G.mod = 1
                    elif len(G.flag) == 10:
                        meantime = 0
                        for x in G.timeList:
                            meantime += x
                        answer = messagebox.showinfo("Finished",
                                                           "Matrix " + str(G.flag[0]) + " Was the fastest- " + str(
                                                               G.timeList[0]) + " seconds\nMatrix " + str(
                                                               G.flag[9]) + " Was the slowest- " + str(G.timeList[
                                                                                                           9]) + " seconds\nMean time for 100% infect: " + str(
                                                               float("{:.3f}".format(
                                                                   meantime / 10))) + "\nClick ok to close")

                        if answer == 'ok':
                            quit()


        for index in range(repeats):
            x = [c[0] for c in G.creatures[index]["healthy"][frame]]
            y = [c[1] for c in G.creatures[index]["healthy"][frame]]
            parts[index * 2].set_data(x, y)

            x = [c[0] for c in G.creatures[index]["infected"][frame]]
            y = [c[1] for c in G.creatures[index]["infected"][frame]]
            parts[index * 2 + 1].set_data(x, y)

            yq = G.creatures[index]["lines"][:frame + 1]
            yg = G.creatures[index]["growth"][:frame + 1]
            xq = np.arange(len(G.creatures[index]["lines"][:frame + 1]))
            # xg = np.true_divide(xq, 1000 / interval)

            parts[repeats * 2 + index].set_data(xq, yq)
            parts[repeats * 3 + index].set_data(xq, yg)
            parts[repeats * 4 + index].set_data(xq, yq)

        return parts

    G.mod = 10
    G.timeList = []
    G.flag = []
    G.starttime = time.time()
    ani = animation.FuncAnimation(fig, animate, frames=G.frames, interval=interval, blit=True, init_func=init)

    plt.show(block=True)


if __name__ == '__main__':
    main()