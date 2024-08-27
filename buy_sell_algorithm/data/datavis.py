import numpy as np
import random
import math
import matplotlib.pyplot as plt

"""
    Trying to model web server data 
"""

# data for 10 cycles
cycles = {0:[[], [], []], 1:[[], [], []], 2:[[], [], []], 3:[[], [], []], 4:[[], [], []], 5:[[], [], []], 6:[[], [], []], 7:[[], [], []], 8:[[], [], []], 9:[[], [], []]}

def get_piecewise_sine(data_points):
    q1 = int(0.25*data_points)
    q2 = int(0.75 * data_points)

    out = [0 for _ in range(q1)] + [np.sin(((i-q1)/(q2-q1))*math.pi) for i in range(q1, q2)] + [0 for _ in range(q1)]

    return out

def get_piecewise_data(data_points):
    q1 = int(0.25*data_points)
    q2 = int(0.75 * data_points)

    out = [1 for _ in range(q1)] + [i//5 for i in range(q1, q2)] + [5 for _ in range(q1)]

    return out

class Data:
    def __init__(self) -> None:
        self.cycle_time = 300  # 5 minutes
        self.random_time = 5   # 5 seconds for new random data
        self.data_points = self.cycle_time // self.random_time
        # self.sines = [np.sin(((i+1)/30)*math.pi) for i in range(self.data_points)]
        self.sines = get_piecewise_sine(self.data_points)
        self.base_demand = get_piecewise_data(self.data_points)

    # randomise all cycles
    def randomise(self):    
        for num, cycle in cycles.items():
            for a in cycle:
                a.clear()
                for i in range(self.data_points):
                    a.append(round(random.randrange(0, 8) + 10*(self.base_demand[i]-self.sines[i]), 2))

    def print_data(self):
        for cycle in cycles.values():
            print(cycle)

    def plot_data(self, data_index):
        times = [i*5 for i in range(self.data_points)]
        figure, axis = plt.subplots(2, len(cycles) // 2)

        for row in range(2):
            for col in range(len(cycles) // 2):
                cycle_num = 5*row + col
                axis[row, col].plot(times, cycles[cycle_num][data_index])
                axis[row, col].set_title(f"Cycle number {cycle_num}")
            
        plt.show()

if __name__ == "__main__":
    d = Data()
    d.randomise()
    d.plot_data(0)
