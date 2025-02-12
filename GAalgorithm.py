'''
Creating crossword mini puzzles using a genetic algorithm and a wordnet-based fitness function

Written by Paul Bodily for Computational Creativity
Python version 3.9.1
'''

import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
import random
import string
import random as rand
import matplotlib.pyplot as plt
from nltk.corpus import words

DIMENSION = 5 # Puzzle dimension (both width and height)
all_fitness_runs = []

def track_fitness(fitness_values):
    all_fitness_runs.append(fitness_values)

def plot_fitness_graph():
    plt.figure(figsize=(10, 6))

    for i, fitness_values in enumerate(all_fitness_runs):
        generations = list(range(len(fitness_values)))
        plt.plot(generations, fitness_values, label=f'Run {i+1}', marker='o')

    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.title("Fitness Progress Across Runs")
    plt.legend()
    plt.grid(True)
    plt.show()


def initialize_crossword():
    return [[random.choice(string.ascii_uppercase) for i in range(DIMENSION)] for j in range(DIMENSION)]


def print_crossword(crossword_to_print):
    for row in crossword_to_print:
        for letter in row:
            print(letter, " ", end='')
        print()


def print_crossword_clues(crossword_to_clue):
    for i in range(DIMENSION):
        word = ''.join(crossword_to_clue[i])
        syns = wordnet.synsets(word)
        if syns:
            print(i+1, "Across:", syns[0].definition(), "(", word, ")")
        else:
            print(i+1, "Across:", word, "is invalid")

    print()

    # Words in cols
    for j in range(DIMENSION):
        word = ''
        for i in range(DIMENSION):
            word += crossword_to_clue[i][j]
        syns = wordnet.synsets(word)
        if syns:
            print(j+1, "Down:", syns[0].definition(), "(", word, ")")
        else:
            print(j+1, "Down:", word, "is invalid")

#need to run this for every generation
#can operate very similarly to the print_crossword_clues function, which checks for definitions
def check_fitness(crossword_to_clue):
    #TODO
    fitness = 0
    #print(crossword_to_clue)
    #print(type(crossword_to_clue))
    # Words in rows
    for i in range(DIMENSION):
        word = ''.join(crossword_to_clue[i])
        syns = wordnet.synsets(word)
        if syns:
            fitness += 1

    #print()

    # Words in cols
    for j in range(DIMENSION):
        word = ''
        for i in range(DIMENSION):
            word += crossword_to_clue[i][j]
        syns = wordnet.synsets(word)
        if syns:
            fitness += 1
    #print(fitness)
    return fitness

def random_genemix(crossword1, crossword2):
  child = [[0 for _ in range(DIMENSION)] for _ in range(DIMENSION)]
  for i in range(DIMENSION):
    for j in range(DIMENSION):
      if random.random() < 0.5:
        child[i][j] = crossword1[i][j]
      else:
        child[i][j] = crossword2[i][j]
  return child

#Need to rewrite the other two functions, idea is to keep actual words and shuffle everything else
def horizontal_genemix(crossword1, crossword2):
    child = [[0 for _ in range(DIMENSION)] for _ in range(DIMENSION)]

    for i in range(DIMENSION):
      word1 = ''.join(crossword1[i])
      word2 = ''.join(crossword2[i])

      is_word1_valid = wordnet.synsets(word1)
      is_word2_valid = wordnet.synsets(word2)

      for j in range(DIMENSION):
        crossover_chance = random.random()

        if is_word1_valid and is_word2_valid:
          if crossover_chance < 0.4:
            child[i][j] = crossword1[i][j]
          elif crossover_chance < 0.8:
            child[i][j] = crossword2[i][j]
          else:
            child[i][j] = crossword1[i][j] if random.random() < 0.5 else crossword2[i][j]

        elif is_word1_valid:
          child[i][j] = crossword1[i][j]
        elif is_word2_valid:
          child[i][j] = crossword2[i][j]
        else:
          child[i][j] = crossword1[i][j] if random.random() < 0.5 else crossword2[i][j]

        if random.random() < 0.05:
          child[i][j] = random.choice(string.ascii_uppercase)

    return child


def vertical_genemix(crossword1, crossword2):
    child = [[0 for _ in range(DIMENSION)] for _ in range(DIMENSION)]

    for j in range(DIMENSION):
        word1 = ''.join(crossword1[i][j] for i in range(DIMENSION))
        word2 = ''.join(crossword2[i][j] for i in range(DIMENSION))

        is_word1_valid = wordnet.synsets(word1)
        is_word2_valid = wordnet.synsets(word2)

        for i in range(DIMENSION):
            crossover_chance = random.random()

            if is_word1_valid and is_word2_valid:
                if crossover_chance < 0.4:
                    child[i][j] = crossword1[i][j]
                elif crossover_chance < 0.8:
                    child[i][j] = crossword2[i][j]
                else:
                    child[i][j] = crossword1[i][j] if random.random() < 0.5 else crossword2[i][j]

            elif is_word1_valid:
                child[i][j] = crossword1[i][j]
            elif is_word2_valid:
                child[i][j] = crossword2[i][j]
            else:
                child[i][j] = crossword1[i][j] if random.random() < 0.5 else crossword2[i][j]


            if random.random() < 0.05:
                child[i][j] = random.choice(string.ascii_uppercase)

    return child

#chance to mutate random letters in the child crosswords
def mutation(crossword):
  #TODO
  for i in range(DIMENSION):
    for j in range(DIMENSION):
      if rand.random() < 0.25: #Don't want mutation rate too high here, otherwise likely to just erase a lot of progress
        crossword[i][j] = random.choice("AEIOU")  #Found a suggestion that common letters might correlate with better fitness improvement over a completely random selection
  return crossword

def select_reproducers(population):
    num_reproducers = max(1, len(population) // 4)
    return population[:num_reproducers]

def plotHistory(history):
  plt.plot(history)
  plt.xlabel("Generation")
  plt.ylabel("Fitness")
  plt.show()

#have number of gens to run, pop size, and number of children per generation
def run_ga(gens, population_size=20, children_per_generation=20):
    '''
    TODO: implement this function

    Function should return a list of (crossword,fitness_score) tuples sorted from highest scoring to lowest scoring

    The code here is just to demonstrate and should be replaced with your own code
    '''

    #population = [(initialize_crossword(), 100), (initialize_crossword(), 250)] #Okay so it looks like this generates two crosswords and attaches an arbitrary fitness score to each of them, giving a tuple
    #Given this, population should run initialize_crossword population_size times for the start
    #after this, we will start an evolutionary process to generate childern based upon some mixing pattern for children.
    #Need to write a function to check fitness of horizontal and vertical lines

    #Checking what the skeleton is doing off the rip
    #print(len(population))
    #print(population[1])

    #initialize actual population
    population = [(initialize_crossword(), 0) for i in range(population_size)]

    #print(population)
    #print(len(population))
    #print(population[0])
    #check_fitness(population[19][0])

    #Writing a GA here since everything else is currently functioning
    #basics of how this might function --> pass in sorted population list --> mate top x% individuals at random until children requirement is met(adding them into pop) --> sort pop based on fitness --> prune to desired size --> repeat for y generations
    fitness_history = []
    for i in range(gens):
      #I guess I'll use the top 25% of pop for mating?
      reproducers = select_reproducers(population)
      #print(reproducers)
      #print(len(reproducers))
      for j in range(children_per_generation):
        mate1 = reproducers[random.randint(0, len(reproducers)-1)]
        mate2 = reproducers[random.randint(0, len(reproducers)-1)]

        #choose mixing method at random
        mix = random.uniform(0,1)
        mut = random.uniform(0,1)
        if mix < 0.5:
          child = vertical_genemix(mate1[0], mate2[0])
        else:
          child = horizontal_genemix(mate1[0], mate2[0])

        #child = random_genemix(mate1[0], mate2[0])

        #decide to do random mutations in the child or not
        if rand.random() < 0.25:
          child = mutation(child)
        population.append((child, check_fitness(child)))

      population.sort(key=lambda x: x[1], reverse=True)
      population = population[0:population_size]
      fitness_history.append(population[0][1])

    #plotHistory(fitness_history)
    return population, fitness_history


if __name__ == '__main__':
  for i in range(8):
    crosswords, fitness_history = run_ga(gens=25000, population_size=20)

    best_crossword = crosswords[0]
    print_crossword(best_crossword[0])
    print("Fitness:", best_crossword[1])
    print("Clues:")
    print_crossword_clues(best_crossword[0])

    track_fitness(fitness_history)

  plot_fitness_graph()