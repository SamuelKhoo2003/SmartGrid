import sys, os

train_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

if train_root not in sys.path:
    sys.path.insert(0, train_root)

from neural_net import Population, neural_net
import numpy as np
from utils import module_from_file, mae, save_population, get_population, add_noise, batch_up, mse, plot_datas
from multiprocessing import Pool
from functools import partial

m_server = module_from_file("server_data", "buy_sell_algorithm/data/server_data.py")
m_made = module_from_file("Data", "buy_sell_algorithm/data/datavis.py")

serve = m_server.server_data()

pool = None

def av(r):
    x, y = r
    return (x+y)//2

class Train:
    """
        Train models using a genetic algorithm to synthesize data if needed, and predict data in a cycle
    """

    def __init__(self, elitism, mutation_prob, mutation_power, max_epochs, num_of_histories, pop_size, nn_batch_size, conc) -> None:
        global pool
        
        self.histories_buffer = {'buy_price':[], 'sell_price':[], 'demand':[]}
        self.data_fitnesses = {'buy_price':0, 'sell_price':0, 'demand':0}
        self.num_of_histories = num_of_histories
        self.fitness_threshold = 0
        self.fitness_buffer = []
        self.epsilon = 0.0001
        self.save_checkpoint = 1
        self.saved_pop_path = os.path.join(train_root, "saved_populations")
        self.saved_graphs_path = os.path.join(train_root, "graphs")
        self.start_index = 0
        self.end_index = 0
        self.current_data_name = ""

        self.elitism = elitism
        self.mutation_prob = mutation_prob
        self.mutation_power = mutation_power
        self.concurrent = conc
        self.epochs = max_epochs

        self.pop_size = pop_size
        self.nn_batch_size = nn_batch_size

        self.nn_batches = batch_up((0, self.pop_size), self.nn_batch_size)
        pool = Pool(processes=len(self.nn_batches))

        self.most_recent = None

        os.makedirs(self.saved_pop_path, exist_ok=True)
        os.makedirs(self.saved_graphs_path, exist_ok=True)

    def add_to_histories_buffer(self, most_recent_histories):
        for k,v in self.histories_buffer.items():
            if(k == "demand"):
                addition = list(map(lambda x : 5*x, most_recent_histories[k]))
            else:
                addition = most_recent_histories[k]

            self.histories_buffer[k] = v[1:] + [addition]

    def first_call(self) -> bool:
        return any([b==[] for b in self.histories_buffer.values()])

    def get_synthetic_data(self, data_type : str, parsed_data) -> tuple[list[list], list]:
        """
            return a tuple of actual data and a set of synthetic data derived from this actual data
        """
        h_data = parsed_data[data_type]

        print("Training to synthesize similar data from one previous cycle")

        out = []
        amount = min(self.num_of_histories, 10)

        pop = Population(2, pop_size=5, input_nodes=2, output_nodes=1, mutation_prob=self.mutation_prob, mutation_power=self.mutation_power, elitism=self.elitism)
        best_model = None
        data_points = 60
        epochs = 20

        checkpoints = list(map(av, batch_up((0,epochs), epochs//self.num_of_histories)))
        check_counter = 0

        # training
        for epoch in range(epochs):
            synthetics = []
            
            for model in pop.models:
                synth = []
                
                for i in range(data_points):
                    if(i == 0): input = [h_data[i+2], h_data[i+1]]
                    elif(i == data_points-1): input = [h_data[i-1], h_data[i-2]]
                    else: input = [h_data[i-1], h_data[i+1]]
            
                    synth.append(model.query(input)[0][0])

                _mse = mse(h_data, synth)

                if(_mse):
                    pop.fitnesses.append(1 / _mse)
                else:
                    pop.fitnesses.append(100000)

                synthetics.append(synth)

            best_model = np.argmax(pop.fitnesses)
        
            if(check_counter < self.num_of_histories and checkpoints[check_counter] == epoch):
                out.append(synthetics[best_model])
                check_counter += 1

            pop = Population(old_pop=pop)

        # plot_datas(out+[h_data], "synth", "data")

        if(data_type == "demand"):
            # multiply all by 5
            out = list(map(lambda x : 5*x, out))
            h_data = list(map(lambda x : x*5, h_data))
        
        return out, h_data
        
    def make_prediction(self, model):
        prediction = []

        for j in range(self.start_index, self.end_index):
            input = []
            for i in range(self.num_of_histories):
                try:
                    input.append(self.training_histories[i][j])

                except Exception as e:
                    print(self.training_histories, i, j)
                    print(e)
                    sys.exit(1)  

            prediction.append(model.query(input)[0][0])

        return prediction
    
    def process_batch(self, batch):
        predictions = []
        fitnesses = []

        for model in batch:
            prediction = self.make_prediction(model)
            predictions.append(prediction)

            _mse = mse(self.most_recent, prediction)

            if(_mse != 0):
                fitnesses.append(1 / _mse)
            else:
                fitnesses.append(100000)

        return fitnesses, predictions

        
    def train_models(self, models : neural_net) -> tuple[list[float], list[float]]:
        """
            Train models on a set of histories and return a tuple lists of each model's fitness, and each model's prediction 
        """

        if(self.concurrent):
            global pool
            
            # concurrently

            batches = [models[x:y] for x, y in self.nn_batches]

            result = pool.map(self.process_batch, batches)

            f, p = zip(*result)

            return sum(f, []), sum(p, [])
        
        else:
            # serially
            predictions = []
            fitnesses = []

            for x, y in self.nn_batches:
                f, p = self.process_batch(models[x:y])
                predictions += p
                fitnesses += f

            return fitnesses, predictions
        
    def train_on_histories(self) -> neural_net:
        """
            given a set of histories, and the most recent history, train to predict the cycle of the 
            most recent history
        """
        best_pred = None
        best_fitness = None
        most_recent_pop = None

        file_name = os.path.join(self.saved_pop_path, self.current_data_name+".pop")
        
        old_pop = get_population(file_name)

        if(old_pop):
            pop = Population(old_pop=old_pop)
            print("Loaded previous best population")
        else:
            input_nodes = self.num_of_histories
            pop = Population(6, pop_size=self.pop_size, input_nodes=input_nodes, output_nodes=1, mutation_prob=self.mutation_prob, 
                            elitism=self.elitism, mutation_power=self.mutation_power)
        
            print("Started from random population")
            
        for epoch in range(self.epochs):
            fitnesses, predictions = self.train_models(pop.models)
            pop.fitnesses = fitnesses

            best_model_index = np.argmax(pop.fitnesses)
            # best_pred = predictions[best_model_index]
            best_fitness = pop.fitnesses[best_model_index]

            if ((self.fitness_threshold != 0) and (best_fitness > self.fitness_threshold)):
                break
            else:
                self.fitness_buffer.append(best_fitness)
            
            print("Best fitness: ", best_fitness)

            most_recent_pop = pop
            pop = Population(old_pop=pop)
            pop.elitism = (epoch+1 / self.epochs)
    
        save_population(most_recent_pop, file_name)   
        self.data_fitnesses[self.current_data_name] = best_fitness

        return pop.models[best_model_index]

    def query_model(self, data_name : str, start_index : int, end_index : int, most_recent : list[float]) -> list[float]:
        """
        - this should be called at the beginning of each cycle to predict values for whole cycle
        - it takes some time:
        - the very first time this is called, the histories buffer will be empty, so it has to synthesize it own for prediction training, which is an extra overhead.
        - Prediction returned will only be between `start_index` and `end_index`
        - Return prediction of next cycle
        """
        print()
        if(data_name in self.histories_buffer):
            previous = self.histories_buffer[data_name]
            
            if(self.data_fitnesses[data_name] != 0): self.fitness_threshold = min(add_noise(self.data_fitnesses[data_name], 2), 100)

            print("Training on the historical data. Training to predict most recent cycle")
            print("Threshold: ", self.fitness_threshold)

            self.start_index = start_index
            self.end_index = end_index
            self.training_histories = previous
            self.most_recent = most_recent
            self.current_data_name = data_name

            # train model to predict the most recent cycle given a set of previous cycles
            best_model = self.train_on_histories()

            prediction = []

            for j in range(start_index, end_index):
                input = []
                for i in range(self.num_of_histories):
                    input.append(self.histories_buffer[data_name][i][j])

                prediction.append(best_model.query(input)[0][0])

            return prediction

        else:
            print("Training on this data not implemented yet")
            sys.exit(1)


