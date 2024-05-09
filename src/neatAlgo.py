import neat
import os

import neat.population

class neatSimulation:

  def __init__(self) :
    self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.getcwd() + "/dinoRunAi/neat_config.txt")
    self.population = neat.Population(self.config)
    self.population.add_reporter(neat.StdOutReporter(True))
  
  def runTraining(self):
    self.population.run(self.runFunction)
    
  def runFunction(self, genomes, config):
    # for genome_id, genome in genomes:

    pass



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