import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import importlib.util
import pickle
import math
from types import ModuleType
import json
from threading import Lock
from typing import Dict
import os

SUNRISE = 15    #Sunrise ticks after start of day
DAY_LENGTH = 30 #Ticks between sunrise and sunset
project_dir = os.getcwd()
lock = Lock()
json_path = os.path.join(project_dir, "react-front-end/src/assets/ExternalInfo.json")
tcp_path = os.path.join(project_dir, "tcp", "data.json")

"""
    Useful helper functions
"""

def pad(array:list[int]) -> int:
    return [0]+array+[0]

def mse(a:list[float], b:list[float]) -> float:
    """
        Mean squared error
    """
    out = 0 
    for x, y in zip(a, b):
        out += ((x - y)**2)
    
    return out / len(b)

def sse(a:float, b:float) -> float:
    """
        Sum of squared errors
    """
    out = 0 
    for x, y in zip(a, b):
        out += (x - y)**2
                
    return out

def mae(a:float, b:float) ->float:
    """
        Mean absolute error
    """
    out = 0 
    for x, y in zip(a, b):
        out += abs(x - y)
    
    return out / len(b)
     
def add_noise(x:float, y:int) -> float:
    """
        Multiply x by y
    """
    return x*y

def plot_datas(datas, title, ylabel, save=True)->None:   
    """
    Pass a list of datas to plot
    set of data on the same graph needs to be put into a list
    """

    times = [i*5 for i in range(0, max(list(map(lambda x : len(x), datas))))]
    colors = cm.rainbow(np.linspace(0, 1, len(datas)))

    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel(ylabel)    
    
    for i in range(len(datas)):
        plt.plot(times[:len(datas[i])], datas[i], colors[i])

    if(save):
        file_name = f"{project_dir}/buy_sell_algorithm/predictions/graphs/{ylabel}"
        plt.savefig(file_name)
        plt.close()
    else:
        plt.show()

def module_from_file(module_name:str, file_path:str)->ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# split a univariate sequence into samples
def split_sequence(sequence:list[float], x_width:int, y_width:int=1) -> tuple[np.array, np.array]:
    X, y = list(), list()
    
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + x_width
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
          
        if(end_ix + y_width > len(sequence)):
            break
        
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:end_ix+y_width]
        X.append(seq_x)
        y.append(seq_y)
          
    return np.array(X), np.array(y)

def save_population(pop, file_name) -> None:
    print("Try saving to ", file_name)

    try:
        with open(file_name, "wb") as f:
            pickle.dump(pop, f)
    except IOError as e:
        print("Could not save population because of ", e)

def get_population(file_name):
    print("Try laoding from ", file_name)

    try:
        with open(file_name, "rb") as f:
            return pickle.load(f)
    except IOError as e:
        print("Could not load population because of ", e)
        return None

def batch_up(_range, width):
    """
        `_range` - tuple of full range to batch up
        `width` - size of a single batch
    """
    out = []
    for i in range(*_range, width):
        out.append((i, i+width))

    return out

def get_sunlight():
    """
        Original: https://github.com/edstott/ICelec50015/blob/main/app.py

        Get sunlight for a tick. To be used on first cycle where we don't have data buffers
    """
    sunlight = []

    for tick in range(60):
        if tick < SUNRISE:
            sunlight.append(0)
        elif tick < SUNRISE + DAY_LENGTH:
            sunlight.append(int(math.sin((tick-SUNRISE)*math.pi/DAY_LENGTH)*100))
        else:
            sunlight.append(0)
            
    return sunlight

def init_frontend_file():
    try:
        initial_data = {str(i): [] for i in range(60)}   # Create keys '0' to '59' with empty lists
        # initial_data["batteryStorage"] = 0
        
        # Write the initial structure to the JSON file
        with open(json_path, "w") as f:
            json.dump(initial_data, f, indent=4)

        print(f"Initialized {json_path} with empty data for ticks 0 to 59.")

    except Exception as e:
        print(f"An error occurred during initialization: {e}")


def add_data_to_frontend_file(data : Dict):
    """
        pass the data you want to be displayed on front end in Python dict
    """
    with lock:  # only one thread can access this at any one time
        if 'tick' not in data:
            raise ValueError("The 'data' dictionary must contain a 'tick' key.")
        
        tick_value = str(data['tick'])  # Convert tick to string to match JSON keys

        try:
            # Check if the file exists
            if not os.path.exists(json_path):
                raise FileNotFoundError(f"The file {json_path} does not exist. Initialize it first.")

            # Read the JSON file
            with open(json_path, "r") as f:
                json_data = json.load(f)

            # Ensure the tick value exists in the JSON data
            if tick_value in json_data:
                # Append new data to the list for the specified tick
                json_data[tick_value].append(data)
            else:
                raise ValueError(f"Tick {tick_value} is not valid. Must be between '0' and '59'.")

            # Write the updated JSON back to the file
            with open(json_path, "w") as f:
                json.dump(json_data, f, indent=4)

            if tick_value == "59":
                print("Tick 59 reached. Clearing data...")
                init_frontend_file()

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from the file {json_path}: {e}")
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    print(get_sunlight())