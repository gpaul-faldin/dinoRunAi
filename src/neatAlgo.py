import neat
import os
import main
import threading
from queue import Queue
import time
import pickle
import statistics
import asyncio

import neat.population

class neatSimulation:

  def __init__(self) :
    self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.getcwd() + "/dinoRunAi/neat_config.txt")
    self.population = neat.Population(self.config)
    self.population.add_reporter(neat.StdOutReporter(True))
    self.best_genome = None
    self.generation = 0
  
  def runTraining(self):
    self.population.run(self.runFunction)
  
  def calculate_fitness(self, score):
    return score / 10000

  def run_genome(self, Simuthread: threading.Thread, genome: neat.DefaultGenome, command_queue: Queue, data_queue: Queue, result_queue: Queue, monitor=False):
    net = neat.nn.FeedForwardNetwork.create(genome, self.config)
    Simuthread.start()
    time.sleep(5)
    command_queue.put('jump')
    
    while Simuthread.is_alive():

        if not data_queue.empty():
          data = data_queue.get()

          dino_x = data['dino']['x']
          dino_y = data['dino']['y']
          obstacle_x = data['obstacle'][0]['x'] if data['obstacle'] else 0
          obstacle_y = data['obstacle'][0]['y'] if data['obstacle'] else 0
          velocity = data['velocity']
        
          outputs = net.activate((dino_x, dino_y, obstacle_x, obstacle_y, velocity))

          if outputs[0] > 0.8:
              command = 'jump'
          elif outputs[0] > 0.5:
              command = 'half-jump'
          else:
              command = ''

          if command != '':
            command_queue.put(command)
        time.sleep(0.00001)

    # Get the final score from the result queue
    score = result_queue.get()
    # print (f"Genome {genome.key} Score: {score}")

    # Calculate the fitness based on the score
    fitness = self.calculate_fitness(score)

    # Set the fitness for this genome
    genome.fitness = fitness

  def log_genome(self, genomes):
    fitnesses = [genome.fitness for _, genome in genomes if genome.fitness is not None]
    avg_fitness = sum(fitnesses) / len(fitnesses)
    rounded_avg_fitness = round(avg_fitness, 4)  # Round average fitness to four decimal places

    std_dev = statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0

    best_genome = max(genomes, key=lambda g: g[1].fitness)
    best_genome_object = best_genome[1]

    rounded_std_dev = round(std_dev, 4)  # Round standard deviation to four decimal places

    filename = f"./dinoRunAi/genome/gen_{self.generation}_fitness{best_genome_object.fitness}_avg_fitness{rounded_avg_fitness}_std_dev{rounded_std_dev}.pkl"

    with open(filename, "wb") as f:
        pickle.dump(best_genome_object, f)


  def runFunction(self, genomes, config):
    best_fitness = 0
    best_genome = None

    threads: list[threading.Thread] = []
    
    monitor = False

    for genome_id, genome in genomes:
        if monitor == False:
          simulation_instance = main.getInstance(f"Genome {genome_id}", True)
        else:
          simulation_instance = main.getInstance(f"Genome {genome_id}")

        Simuthread, command_queue, data_queue, result_queue = simulation_instance[0], simulation_instance[1], simulation_instance[2], simulation_instance[3]
        if monitor == False:
          trainingThread = threading.Thread(target=self.run_genome, args=(Simuthread, genome, command_queue, data_queue, result_queue, True))
          monitor = True
        else:
          trainingThread = threading.Thread(target=self.run_genome, args=(Simuthread, genome, command_queue, data_queue, result_queue))
        threads.append(trainingThread)
        trainingThread.start()

    for thread in threads:
        thread.join()

    if self.generation % 10 == 0:
      self.log_genome(genomes)
    self.generation += 1




neatInstance = neatSimulation()
neatInstance.runTraining()


# def neat_init():

# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.getcwd() + "/dinoRunAi/neat_config.txt")

# population = neat.Population(config)

# population.add_reporter(neat.StdOutReporter(True))

# def run(genome, config):
    
#     pass

# # def evaluate_network(network, config):
# #     pass

# population.run(run)

# bestNewtwork = neat_instance.best_genome()