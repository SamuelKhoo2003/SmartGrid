import numpy as np

"""
    Neural net class and genetic algorithm 
"""

class neural_net:
    def __init__(self, *args, **kwargs):
        # initialise weight matrices
        if("weight_matrices" in kwargs):
            self.weight_matrices = kwargs["weight_matrices"]
        else:
            layers = (kwargs["input_nodes"], *args, kwargs["output_nodes"],)

            self.weight_matrices = []

            for n in range(len(layers)-1):
                self.weight_matrices.append(np.random.normal(0.0, pow(layers[n], -0.5), (layers[n+1], layers[n])))

    def activation_func(self, x):
        return np.array([i * (i > 0) for i in x])

    def query(self, input_list):
        h_hat = np.array(input_list, ndmin=2).T
        
        for wm in self.weight_matrices:
            h = np.matmul(wm, h_hat)
            h_hat = self.activation_func(h)

        return h_hat
    
"""
    Initialise a population of neural nets, pass in the population size, number of input neurons for each neural net,
    number of output neurons for each neural net
"""
class Population:
    def __init__(self, *args, **kwargs):        
        if "old_pop" not in kwargs:
            self.size = kwargs["pop_size"]
            self.models = [neural_net(*args, input_nodes=kwargs["input_nodes"], output_nodes=kwargs["output_nodes"]) for _ in range(self.size)]
            self.input_nodes = kwargs["input_nodes"]
            self.hidden_nodes = args
            self.output_nodes = kwargs["output_nodes"]

            self.mutation_prob = kwargs["mutation_prob"]
            self.elitism = kwargs["elitism"]
            self.mutation_power = kwargs["mutation_power"]

        else:
            old_population = kwargs["old_pop"]

            self.size = old_population.size
            self.input_nodes = old_population.input_nodes
            self.hidden_nodes = old_population.hidden_nodes
            self.output_nodes = old_population.output_nodes

            self.mutation_prob = old_population.mutation_prob if ("mutation_prob" not in kwargs) else kwargs["mutation_prob"]
            self.elitism = old_population.elitism if ("elitism" not in kwargs) else kwargs["elitism"]
            self.mutation_power = old_population.mutation_power if ("mutation_power" not in kwargs) else kwargs["mutation_power"]

            self.old_models = old_population.models
            self.old_fitnesses = old_population.fitnesses

            self.models = []
            self.crossover()
            self.mutate()

        self.fitnesses = []

    def crossover(self):
        # setup higher probabilities for higher performing neural nets
        sum_of_fitnesses = np.sum(self.old_fitnesses)
        probs = [self.old_fitnesses[i]/sum_of_fitnesses for i in range(self.size)]

        for i in range(self.size):
            if i < self.size*self.elitism:
                # sort by order of fitness (descending)
                fitness_indices = np.argsort(probs)[::-1]
                # if model within elitism critical region, select it as is
                child = self.old_models[fitness_indices[i]]
            else:
                # select 2 best performing fitness indices using probs, do not replace,
                # so indices cannot be selected twice
                a, b = np.random.choice(self.size, size=2, p=probs, replace=False)

                # setup models from those indices
                parent_a, parent_b = self.old_models[a], self.old_models[b]
                child = neural_net(*self.hidden_nodes, input_nodes=self.input_nodes, output_nodes=self.output_nodes) 
                a_fitness, b_fitness = self.old_fitnesses[a], self.old_fitnesses[b]

                if a_fitness == 0 and b_fitness == 0:
                    prob_from_a = 0.5

                    for wm in child.weight_matrices:
                        for row_ind, row in enumerate(wm):
                            for col_ind, col in enumerate(row):
                                if np.random.random() < prob_from_a:
                                    wm[row_ind][col_ind] = parent_a.wi_ha[row_ind][col_ind]
                                else:
                                    wm[row_ind][col_ind] = parent_b.wi_ha[row_ind][col_ind]
                else:
                    for i in range(len(child.weight_matrices)):
                        wm = (a_fitness/(a_fitness+b_fitness))*parent_a.weight_matrices[i] + (b_fitness/(a_fitness+b_fitness))*parent_b.weight_matrices[i]

            # add new object to population
            self.models.append(child)

    def mutate(self):
        for model in self.models:
            for wm in model.weight_matrices:
                for row in wm:
                    for ind, col in enumerate(row):
                        if np.random.random() < self.mutation_prob:
                            row[ind] += np.random.uniform(-self.mutation_power, self.mutation_power)
                
                """
                rands = np.random.uniform(-self.mutation_power, self.mutation_power, size=wm.shape)
                mask = np.random.random(wm.shape) < self.mutation_prob

                wm = np.where(mask, wm + rands, wm)
                """

