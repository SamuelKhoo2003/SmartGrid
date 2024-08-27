import data.server_data as data
from predictions.train import Train
import time
import optimization as opt

'''
most naive solution to the problem
'''
deferable_list = []

def naive_smart_grid_optimizer(data_buffers, t, curr_storage, deferables, unmet_demand):
    current_storage = curr_storage
    STORAGE_CAPACITY = 50  # Maximum storage capacity in Joules
    POWER_LOSS = 2
    LINEAR_SOLAR_DEPENDANCE = 5/100
    global deferable_list
    total_profit = 0

    if deferables:
        deferable_list = opt.parseDeferables(deferables)
    
    solar_energy = data_buffers['sun'][-1] * LINEAR_SOLAR_DEPENDANCE
    actual_demand = data_buffers['demand'][-1] + POWER_LOSS
    buy_price = data_buffers['buy_price'][-1]/100
    sell_price = data_buffers['sell_price'][-1]/100

    # Total energy needed
    total_demand = actual_demand + unmet_demand
    for idx in range(len(deferable_list)):
        start = max(deferable_list[idx].start - t, 0)
        end = deferable_list[idx].end - t
        if start <= t < end:
            total_demand += deferable_list[idx].energyTotal / (end - start) # Spread energy requirement over time window

    excess_energy = 0
    if total_demand > 20:
        unmet_demand = total_demand - 20
        total_demand = 20

    print(f"naive demand: {total_demand}")
    # Use solar energy first to meet demand
    if solar_energy >= total_demand:
        solar_energy -= total_demand
        total_demand = 0
    else:
        total_demand -= solar_energy
        solar_energy = 0

    # Use stored energy if solar is insufficient
    if total_demand > 0:
        if current_storage >= total_demand:
            current_storage -= total_demand
            total_demand = 0
        else:
            total_demand -= current_storage
            current_storage = 0

    # Buy energy from the grid if necessary
    if total_demand > 0:
        # Buy enough energy to meet the remaining demand
        energy_bought = total_demand
        total_profit -= energy_bought * sell_price # Subtract the cost of buying energy
        total_demand = 0

    # Handle excess solar energy
    if solar_energy > 0:
        # First try to store the excess energy
        if current_storage + solar_energy <= STORAGE_CAPACITY:
            current_storage += solar_energy
        else:
            # If storage is full, sell the excess energy
            # excess_energy = solar_energy
            excess_energy = current_storage + solar_energy - STORAGE_CAPACITY
            total_profit += excess_energy * buy_price # Add the revenue from selling energy
            current_storage = STORAGE_CAPACITY
        solar_energy = 0

    # Print current state for debugging
    print("for tick: " + str(t))
    print(f"Time {t}: Demand={total_demand}, Solar={solar_energy}, Storage={current_storage}, Buy Price={buy_price}, Sell Price={sell_price}")

    return total_profit, current_storage, unmet_demand

if __name__ == "__main__":
    # Run the optimizer
    print("Running naive")