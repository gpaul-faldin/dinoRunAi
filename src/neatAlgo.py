import neat
import os
import main
import threading
from queue import Queue
import time
import math

import neat.population

class neatSimulation:

  def __init__(self) :
    self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.getcwd() + "/dinoRunAi/neat_config.txt")
    self.population = neat.Population(self.config)
    self.population.add_reporter(neat.StdOutReporter(True))
  
  def runTraining(self):
    self.population.run(self.runFunction)
  
  def calculate_fitness(self, score):
    return 1 / (1 + math.exp(-score / 1000))

  def run_genome(self, Simuthread: threading.Thread, genome: neat.DefaultGenome, command_queue: Queue, data_queue: Queue, result_queue: Queue):
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

          if outputs[0] > 0.7:
            command_queue.put('jump')
          elif outputs[0] > 0.3:
            command_queue.put('half-jump')
        time.sleep(0.00001)

    # Get the final score from the result queue
    score = result_queue.get()

    # Calculate the fitness based on the score
    fitness = self.calculate_fitness(score)

    # Set the fitness for this genome
    genome.fitness = fitness

  def runFunction(self, genomes, config):

    threads: list[threading.Thread] = []

    for genome_id, genome in genomes:

        simulation_instance = main.getInstance(f"Genome {genome_id}")

        Simuthread, command_queue, data_queue, result_queue = simulation_instance[0], simulation_instance[1], simulation_instance[2], simulation_instance[3]

        trainingThread = threading.Thread(target=self.run_genome, args=(Simuthread, genome, command_queue, data_queue, result_queue))
        threads.append(trainingThread)
        trainingThread.start()
    for thread in threads:
        thread.join()



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