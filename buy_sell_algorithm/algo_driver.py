from queue import Queue
import time
from predictions.utils import plot_datas, get_sunlight, init_frontend_file, add_data_to_frontend_file
from colorama import Fore, Back, Style, init
import optimization as opt
from predictions.train import Train
from data.server_data import server_data
import naive_solution as naive
from threading import Lock
import sys
from typing import Dict
import random
import requests
import optimization2 as opt2

# Initialize colorama
init(autoreset=True)

class Algorithm:
    def __init__(self) -> None:
        self.serve = server_data()
        self.trainer = Train(elitism=0.2, mutation_prob=0.08, mutation_power=0.1, max_epochs=20, num_of_histories=5, 
                pop_size=225, nn_batch_size=15, conc=True)

        self.data_buffers : Dict[str, list[float]] = {'buy_price':[], 'sell_price':[], 'demand':[], 'sun':[]}
        self.old_predictions : Dict[str, list[float]] = {'buy_price':[], 'sell_price':[], 'demand':[], 'sun':[]}
        self.predictions : Dict[str, list[float]] = {'buy_price':[], 'sell_price':[], 'demand':[], 'sun':[]}
        self.next_predictions : Dict[str, list[float]] = {'buy_price':[], 'sell_price':[], 'demand':[], 'sun':[]}
        self.defs = None

        self.cycle_count = 0
        
        self.starting_tick, _ = self.serve.tick_finder(0, init=True)

        if(self.serve.error):
            print(Back.CYAN + "Tick value got is incorrect, start again")

        self.window_allowance = 4
        self.tick = self.starting_tick
        self.data_batch_size = 15
        self.buy_to_sell_ratio = 0.5
        self.computation_time = 1.5

        self.trade_url = "https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessTradeLog"
        self.energy_url = "https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog"

    def trade_api_post(self, day, earnings, energysold, energybought):
        data = {
            "dayID": day,
            "earnings": earnings,
            "energySold": energysold,
            "energyBought": energybought
        }
        try:
            response = requests.post(self.trade_url, json=data)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            print("POST request successful!")
        except requests.exceptions.RequestException as e:
            print("POST reques failed:", e)

    def energy_api_post(self, day, demand, energyProduced):
        data = {
            "dayID": day,
            "energyUsed": demand,
            "energyProduced": energyProduced
        }

        try:
            response = requests.post(self.energy_url, json=data)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            print("POST request successful!")
        except requests.exceptions.RequestException as e:
            print("POST request failed:", e)
        
    def add_to_data_buffers(self):
        start = time.time()
        self.serve.live_data()
        for data_name, data in self.data_buffers.items():
            #if(data_name == "demand"):
            #    print(self.serve.parsed_data[data_name])
            data.append(self.serve.parsed_data[data_name])

        return time.time() - start

    def new_cycle(self):
        """
            - Set prediction of current cycle to be the most recent history if this is first call to trainer at tick 0
            - If this is not first call to trainer at tick 0, then next predictions should become current predictions
            - Empty data and next predictions buffers, add current values into data buffers to begin with
        """
        start = time.time()

        # at start of new cycle, prepare predictions for current cycle, and set correct historical data
        self.serve.set_historical_prices()
    
        if(self.trainer.first_call()):
            print("First call, assume predictions for all data is most recent cycle")
            
            for data_name, _ in self.trainer.histories_buffer.items():
                previous, most_recent = self.trainer.get_synthetic_data(data_name, self.serve.parsed_data)
                self.trainer.histories_buffer[data_name] = previous[1:] + [most_recent]
                self.predictions[data_name] = most_recent
                self.old_predictions[data_name] = most_recent

            self.predictions['sun'] = get_sunlight()
            self.old_predictions['sun'] = get_sunlight()
            self.defs = None
            
        else:
            print("Current predictions are ready")
            self.old_predictions = self.predictions
            self.old_predictions['sun'] = self.data_buffers['sun']
            self.predictions = self.next_predictions.copy()
            self.predictions['sun'] = self.data_buffers['sun']
            self.trainer.add_to_histories_buffer(self.serve.parsed_data)

        if(self.data_buffers != {'buy_price':[], 'sell_price':[], 'demand':[], 'sun':[]}):
            # previous cycle data buffers are full, we also have what we predicted in self.old_predictions
            for n, p in self.old_predictions.items():
                try:
                    plot_datas([p, self.data_buffers[n]], "Prediction of previous cycle vs Actual data after", n+str(self.cycle_count))
                except Exception as e:
                    print(f"Exception: {e}")
                    print(len(self.data_buffers[n]), len(p))
        
        # empty data and next prediction buffers
        for data_name in ['buy_price', 'sell_price', 'demand', 'sun']:
            self.next_predictions[data_name] = []
            self.data_buffers[data_name] = []

        self.serve.deferables()
        self.defs = self.serve.parsed_data['deferables']

        return time.time() - start

    def prepare_next(self):
        """
            - Prepare predictions for the next cycle using the data buffers you have so far
            - Also add value at current tick into data buffer
        """
        start = time.time()
        
        if(not ((self.starting_tick % self.data_batch_size == 0) and self.trainer.first_call())):
            if((0 < self.tick  - self.starting_tick < self.data_batch_size) and self.trainer.first_call()):
                dist = self.tick - self.starting_tick
            else:
                dist = self.data_batch_size

            if(self.tick == 59):
                x, y = 60-dist, 60
            else:
                x, y = self.tick-dist, self.tick

            for data_name in ['sell_price', 'demand']:
                if(self.next_predictions[data_name] == [] and x != 0):
                    self.next_predictions[data_name] = self.trainer.histories_buffer[data_name][-1][:x]
                
                self.next_predictions[data_name] += self.trainer.query_model(data_name, x, y, self.data_buffers[data_name][x:y])

                assert(len(self.next_predictions[data_name]) % self.data_batch_size == 0)

                print(x, y, len(self.next_predictions[data_name]), data_name)

            self.next_predictions['buy_price'] = list(map(lambda x : x*self.buy_to_sell_ratio, self.next_predictions['sell_price']))

        return time.time()-start

    def something_else(self, naive_storage, storage, unmet_demands, total_profit, total_naive_profit):
        start = time.time()

        time_taken = self.add_to_data_buffers()

        print(Fore.MAGENTA + f"Adding to data buffers took {time_taken} s")

        if(self.trainer.first_call()):
            self.serve.set_historical_prices()

            for data_name in ['buy_price', 'sell_price', 'demand']:
                previous, most_recent = self.trainer.get_synthetic_data(data_name, self.serve.parsed_data)
                self.trainer.histories_buffer[data_name] = previous[1:] + [most_recent]
                self.predictions[data_name] = most_recent

            self.serve.deferables()
            self.defs = self.serve.parsed_data['deferables']
        else:
            self.defs = None

        algovar = opt2.maximize_profit_mpc(storage, self.data_buffers, self.predictions, self.tick, 60-self.tick, self.defs)
        naive_profit, naive_storage, unmet_demands = naive.naive_smart_grid_optimizer(self.data_buffers, self.tick, naive_storage, self.defs, unmet_demands)

        storage = algovar.storage
        total_profit += algovar.profit
        total_naive_profit += naive_profit

        print(f"opt profit (tick): {algovar.profit}")
        print(f"naive profit (tick): {naive_profit}")
        print(f"opt profit total: {total_profit}")
        print(f"naive profit total: {total_naive_profit}")

        print(f" ***************************************************************************************")
       
        add_data_to_frontend_file({"tick": algovar.tick, "naiveProfit": -naive_profit, "optProfit": -algovar.profit, "storage": algovar.storage,"energyTransaction":algovar.optimal_energy_transactions, "energyUsed": algovar.demand, "noDefEnergyUsed": algovar.base_demand,"energyIn": algovar.solar_energy, "storageProfit": -algovar.profit-algovar.storage*algovar.buy_price})

        #Post data to the cloud
        if self.tick == 59:
            if algovar.optimal_energy_transactions > 0:
                energy_sold = 0
                energy_bought = algovar.optimal_energy_transactions
            else:
                energy_sold = algovar.optimal_energy_transactions
                energy_bought = 0
            self.trade_api_post(self.cycle_count, total_profit, energy_sold, energy_bought) #energy sold,energy bought
            self.energy_api_post(self.cycle_count, algovar.demand, algovar.solar_energy) #energy used, energy produced
            total_profit, total_naive_profit = 0, 0

        return time.time() - start + time_taken, naive_storage, storage, total_profit, total_naive_profit, unmet_demands, algovar
    
    def driver(self, q : Queue):
        # fill data buffers with historical data at beginning
        if(self.starting_tick != 0):
            for k, v in self.data_buffers.items():
                if(self.serve.parsed_data[k] != []):
                    if(k == "demand"):
                        self.data_buffers[k] = list(map(lambda x : 5*x, self.serve.parsed_data[k][:self.starting_tick]))
                    else:
                        self.data_buffers[k] = self.serve.parsed_data[k][:self.starting_tick]
                else:
                    self.data_buffers[k] = [0]*self.starting_tick

        print("Started at tick ", self.starting_tick)
        init_frontend_file()
        print("Initialized frontend file")
        remainder = 0
        naive_storage = 0
        storage = 0
        unmet_demand = 0
        total_profit = 0
        total_naive_profit = 0

        loads_data = [{"client": "load", "power":None},{"client": "load1", "power":None, "tick": None}, {"client": "load2", "power":None}, {"client": "load3", "power":None}]
        bidirectional_data = {'client':'bidirectional', 'buysell':None, 'storage':None}

        #data_to_clients = {"load":0, "load1":0, "load2":0, "load3":0, "bidirectional":{"buysell":0, "storage":None}}

        while True: 
            print(f"Current tick {self.tick}")

            if(self.tick == 0):
                self.cycle_count += 1

                print()
                
                # new cycle should always come before something_else such that data buffers get emptied
                time_taken = self.new_cycle()
                tt, naive_storage, storage, total_profit, total_naive_profit, unmet_demand, algovar = self.something_else(naive_storage, storage, unmet_demand, total_profit, total_naive_profit)
                time_taken += tt
                remainder = 5-time_taken 
                print("Cycle ", self.cycle_count)
                print(Fore.MAGENTA + f"Setting up new cycle took {time_taken} s", (Fore.GREEN if remainder > 1.5 else Fore.LIGHTRED_EX) + f"Time to t+1 [{remainder} s]")

            elif((self.tick % self.data_batch_size) == 0 or (self.tick == 59)):
                time_taken, naive_storage, storage, total_profit, total_naive_profit, unmet_demand, algovar = self.something_else(naive_storage, storage, unmet_demand, total_profit, total_naive_profit)
                time_taken += self.prepare_next()
                remainder = 5-time_taken
                print("Cycle ", self.cycle_count)
                print(Fore.YELLOW + f"Preparation and decision took {time_taken} s", (Fore.GREEN if remainder > 1.5 else Fore.LIGHTRED_EX) + f"Time to t+1 [{remainder} s]")
            
            else:
                time_taken, naive_storage, storage, total_profit, total_naive_profit, unmet_demand, algovar= self.something_else(naive_storage, storage, unmet_demand, total_profit, total_naive_profit)
                remainder = 5-time_taken
                print("Cycle ", self.cycle_count)
                print(Fore.BLUE + f"Something else and adding to data buffers took {time_taken} s", (Fore.GREEN if remainder > 1.5 else Fore.LIGHTRED_EX) + f"Time to t+1 [{remainder} s]")

            # we know the time take for computation, and the remainder of time to the next tick
            window_length_in_s = (5+self.computation_time) - max(self.computation_time, time_taken)
            time_to_sleep_in_s = max(0, self.computation_time - time_taken)

            print(Fore.CYAN + f"Hardware given window of {window_length_in_s} s")
            print(Fore.LIGHTGREEN_EX + f"Sending decision to hardware after {time_to_sleep_in_s} s")
            print("********************************************************************************", storage)

            # send decision to hardware when window starts
            time.sleep(time_to_sleep_in_s)

            power = random.uniform(0, 1.5)

            tcp_fake_storage = random.uniform(0, 1.5)

            
            while(not q.empty()):
                _ = q.get()
            #if(q.empty()):
            print("Adding results to queue")
            """
            if algovar.optimal_energy_transactions > 0:
                bidirectional_data['buysell'] = True
            else:
                bidirectional_data['buysell'] = False
            bidirectional_data['storage'] = algovar.optimal_storage_transactions
        `   """
            
            bidirectional_data["buysell"] = False
            bidirectional_data["storage"] = storage

            q.put(bidirectional_data)
            #add_data_to_tcp_algo_file(bidirectional_data)

            for ld in loads_data:
                ld["power"] = algovar.demand/3
                ld["tick"] = self.tick
                q.put(ld)
            
            remainder -= time_to_sleep_in_s

            if(time_taken > 5+self.computation_time):
                print(Fore.RED + "Something took too much time ", time_taken)
                print(Fore.RED + "Final tick was ", self.tick)
                sys.exit(1)

            else:
                # look for new tick
                old_tick = self.tick
                self.tick, polling_time = self.serve.tick_finder(old_tick)

                print(Back.LIGHTBLACK_EX + f"Polling time: {polling_time} s")
                
                if(self.serve.error):
                    if(polling_time < remainder):
                        time.sleep(remainder-polling_time) 
                        
                    self.tick = (self.tick + 1) % 60 

                diff = old_tick - self.tick

                print(Back.LIGHTYELLOW_EX + f"old: {old_tick}, new: {self.tick}")
                
if __name__ == "__main__":
    q = Queue()

    algo = Algorithm()
    algo.driver(q)
